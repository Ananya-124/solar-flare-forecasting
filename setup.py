import os

# Define the directory structure
structure = {
    "models": ["tft_model.ckpt", "scaler.pkl"],
    "src": {
        "preprocess": ["process_solexs.py", "process_hel1os.py", "merge_data.py"],
        "features": ["create_features.py"],
        "training": ["prepare_tft.py", "train_tft.py"],
        "inference": ["predict.py"],
        "utils": ["helpers.py"]
    },
    "dashboard": ["app.py"]
}

# Root level files
root_files = ["src/config.py", "requirements.txt", "main.py"]

def create_structure(base_path="."):
    # Create subdirectories and files
    for folder, contents in structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        
        if isinstance(contents, list):
            for file in contents:
                file_path = os.path.join(folder_path, file)
                if not os.path.exists(file_path):
                    with open(file_path, 'w') as f:
                        f.write(f"# Placeholder for {file}")
        elif isinstance(contents, dict):
            for subfolder, files in contents.items():
                subfolder_path = os.path.join(folder_path, subfolder)
                os.makedirs(subfolder_path, exist_ok=True)
                for file in files:
                    file_path = os.path.join(subfolder_path, file)
                    if not os.path.exists(file_path):
                        with open(file_path, 'w') as f:
                            f.write(f"# Placeholder for {file}")

    # Create root files
    for file in root_files:
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write(f"# Placeholder for {file}")

if __name__ == "__main__":
    create_structure()
    print("Project structure initialized successfully.")
    
    
    import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Solar Flare Forecasting",
    page_icon="☀️",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/final/tft_dataset.csv"
    )

    df["datetime"] = pd.to_datetime(
        df["datetime"]
    )

    return df


df = load_data()

# =====================================================
# HEADER
# =====================================================

st.markdown(
    """
    <div style="
        background: linear-gradient(90deg,#0f172a,#1e293b);
        padding:25px;
        border-radius:15px;
        text-align:center;
        margin-bottom:20px;
    ">
        <h1 style="color:white;">
            ☀️ ADITYA-L1 SOLAR FLARE FORECASTING SYSTEM
        </h1>


    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("Dashboard Controls")

window = st.sidebar.slider(
    "Display Last N Samples",
    min_value=100,
    max_value=len(df),
    value=min(3000, len(df))
)

display_df = df.tail(window)

# =====================================================
# CURRENT VALUES
# =====================================================

latest_soft = display_df["soft_counts"].iloc[-1]
latest_hard = display_df["hard_counts"].iloc[-1]

# Temporary flare probability
flare_prob = min(
    100,
    round(
        (
            latest_soft
            /
            display_df["soft_counts"].max()
        ) * 100,
        2
    )
)

if flare_prob > 80:
    status = "CRITICAL"

elif flare_prob > 50:
    status = "WARNING"

else:
    status = "NORMAL"

# =====================================================
# TOP METRICS
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "☀️ Soft X-Ray",
        f"{latest_soft:.2f}"
    )

with col2:
    st.metric(
        "⚡ Hard X-Ray",
        f"{latest_hard:.2f}"
    )

with col3:
    st.metric(
        "🚨 Flare Probability",
        f"{flare_prob:.2f}%"
    )

with col4:
    st.metric(
        "🌍 Space Weather",
        status
    )

# =====================================================
# ALERT
# =====================================================

if flare_prob > 80:

    st.error(
        "🚨 CRITICAL ALERT : High probability of solar flare activity."
    )

elif flare_prob > 50:

    st.warning(
        "⚠ Elevated solar activity detected."
    )

else:

    st.success(
        "✅ Solar activity currently normal."
    )

# =====================================================
# GAUGE
# =====================================================

st.subheader("🚀 TFT Forecast Confidence")

gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=flare_prob,

        title={
            "text":
            "Solar Flare Probability (Next 30 Minutes)"
        },

        gauge={

            "axis": {
                "range": [0, 100]
            },

            "steps": [

                {
                    "range": [0, 50],
                    "color": "#2ecc71"
                },

                {
                    "range": [50, 80],
                    "color": "#f39c12"
                },

                {
                    "range": [80, 100],
                    "color": "#e74c3c"
                }
            ],

            "threshold": {
                "line": {
                    "width": 4
                },

                "thickness": 0.8,

                "value": flare_prob
            }
        }
    )
)

gauge.update_layout(
    height=350
)

st.plotly_chart(
    gauge,
    use_container_width=True
)

# =====================================================
# COMBINED CATALOGUE
# =====================================================

st.subheader("📡 Combined Solar Activity Catalogue")

combined = display_df.copy()

combined["soft_norm"] = (
    combined["soft_counts"]
    /
    combined["soft_counts"].max()
)

combined["hard_norm"] = (
    combined["hard_counts"]
    /
    combined["hard_counts"].max()
)

fig_combined = go.Figure()

fig_combined.add_trace(
    go.Scatter(
        x=combined["datetime"],
        y=combined["soft_norm"],
        name="SoLEXS",
        line=dict(width=3)
    )
)

fig_combined.add_trace(
    go.Scatter(
        x=combined["datetime"],
        y=combined["hard_norm"],
        name="HEL1OS",
        line=dict(width=3)
    )
)

fig_combined.update_layout(
    title="Combined Solar Activity Timeline",
    height=500,
    xaxis_title="Time",
    yaxis_title="Normalized Intensity"
)

st.plotly_chart(
    fig_combined,
    use_container_width=True
)

# =====================================================
# LIGHT CURVES
# =====================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("☀️ SoLEXS Light Curve")

    fig_soft = px.line(
        display_df,
        x="datetime",
        y="soft_counts"
    )

    st.plotly_chart(
        fig_soft,
        use_container_width=True
    )

with col2:

    st.subheader("⚡ HEL1OS Light Curve")

    fig_hard = px.line(
        display_df,
        x="datetime",
        y="hard_counts"
    )

    st.plotly_chart(
        fig_hard,
        use_container_width=True
    )

# =====================================================
# FLARE CATALOGUE
# =====================================================

st.subheader("🔥 Automated Solar Flare Catalogue")

flare_catalogue = df[
    df["flare"] == 1
][
    [
        "datetime",
        "soft_counts",
        "hard_counts"
    ]
]

st.dataframe(
    flare_catalogue,
    use_container_width=True
)

# =====================================================
# STRONGEST EVENTS
# =====================================================

st.subheader("🏆 Top 10 Strongest Solar Events")

top10 = (
    df.sort_values(
        "soft_counts",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top10[
        [
            "datetime",
            "soft_counts",
            "hard_counts"
        ]
    ],
    use_container_width=True
)

# =====================================================
# STATISTICS
# =====================================================

st.subheader("📊 Mission Statistics")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Total Samples",
        len(df)
    )

with c2:
    st.metric(
        "Detected Flares",
        int(df["flare"].sum())
    )

with c3:
    st.metric(
        "Future Flare Targets",
        int(df["target"].sum())
    )

# =====================================================
# DISTRIBUTION
# =====================================================

st.subheader("📈 Soft X-Ray Distribution")

hist = px.histogram(
    df,
    x="soft_counts",
    nbins=50
)

st.plotly_chart(
    hist,
    use_container_width=True
)

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown(
    """
    **Data Sources:** Aditya-L1 SoLEXS + HEL1OS
    
    **Forecast Model:** Temporal Fusion Transformer (TFT)
    
    **Objective:** Forecast Solar Flares within the next 30 minutes
    """
)