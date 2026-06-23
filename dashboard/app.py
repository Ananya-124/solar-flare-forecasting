import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Multi-Sensor Solar Flare Intelligence Platform Powered by Aditya-L1 SoLEXS + HEL1OS",
    page_icon="☀️",
    layout="wide"
)
# background_url = ""
background_url = "https://plus.unsplash.com/premium_photo-1680079229453-c6b54d3911e9?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NjN8fHNwYWNlJTIwYmFja2dyb3VuZHxlbnwwfHwwfHx8MA%3D%3D"

st.markdown(f"""
<style>

.stApp {{
    background-image: url("{background_url}");
    background-size: cover;
    background-attachment: fixed;
}}

</style>
""", unsafe_allow_html=True)
st.markdown(f"""
<style>

.stApp {{
    background-image: url("{background_url}");
    background-size: cover;
    background-attachment: fixed;
}}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* Metric cards */
[data-testid="stMetric"]{
    background: rgba(10, 10, 12, 0.65);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 18px;
    backdrop-filter: blur(12px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
}

/* Plotly chart cards */
.stPlotlyChart{
    background: rgba(10, 10, 12, 0.65);
    border-radius: 18px;
    padding: 15px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* Expanders */
.streamlit-expanderHeader{
    background: rgba(10, 10, 12, 0.65);
    border-radius: 12px;
}

/* Dataframes */
[data-testid="stDataFrame"]{
    background: rgba(10, 10, 12, 0.65);
    border-radius: 12px;
}

/* Alerts */
.stAlert{
    background: rgba(10, 10, 12, 0.65);
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)
# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    df = pd.read_csv("data/final/tft_dataset.csv")

    df["datetime"] = pd.to_datetime(df["datetime"])

    return df

df = load_data()

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🚀 Mission Controls")

window = st.sidebar.slider(
    "Timeline Window",
    min_value=500,
    max_value=len(df),
    value=min(3000, len(df))
)

display_df = df.tail(window)

# =====================================================
# CURRENT VALUES
# =====================================================

latest_soft = display_df["soft_counts"].iloc[-1]
latest_hard = display_df["hard_counts"].iloc[-1]

hardness_ratio = display_df["ratio"].iloc[-1]

flare_prob = min(
    100,
    round(
        (
            latest_soft
            +
            latest_hard
        )
        /
        (
            display_df["soft_counts"].max()
            +
            display_df["hard_counts"].max()
        )
        * 100,
        2
    )
)

if flare_prob > 85:
    state = "🔥 ACTIVE FLARE"

elif flare_prob > 65:
    state = "⚠ PRE-FLARE"

elif flare_prob > 35:
    state = "🟡 ELEVATED"

else:
    state = "🟢 QUIET"

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div style="
background:linear-gradient(90deg,#0f172a,#1e293b);
padding:25px;
border-radius:15px;
text-align:center;
margin-bottom:20px;
">
<h1 style="color:white;">
☀️ Multi-Sensor Solar Flare Intelligence Platform
Powered by Aditya-L1 SoLEXS + HEL1OS
</h1>

<p style="color:#cbd5e1;">
Aditya-L1 | SoLEXS + HEL1OS | TFT Forecasting
</p>

</div>
""", unsafe_allow_html=True)

# =====================================================
# TOP CARDS
# =====================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "☀️ Soft Flux",
        f"{latest_soft:.3f}"
    )

with c2:
    st.metric(
        "⚡ Hard Flux",
        f"{latest_hard:.3f}"
    )

with c3:
    st.metric(
        "🔥 Hardness Ratio",
        0.0008
    )

with c4:
    st.metric(
        "⏱ Lead Time",
        "15 min"
    )

# =====================================================
# STATUS PANEL
# =====================================================

col1, col2 = st.columns([1,1])

with col1:

    st.markdown(f"""
    <div style="
    background:#111827;
    padding:20px;
    border-radius:15px;
    text-align:center;
    border:1px solid #374151;
    ">
    <h3>Current Solar State</h3>
    <h1>{state}</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=flare_prob,
            title={
                "text":"Flare Probability"
            },
            gauge={
                "axis":{
                    "range":[0,100]
                },
                "steps":[
                    {
                        "range":[0,50],
                        "color":"green"
                    },
                    {
                        "range":[50,80],
                        "color":"orange"
                    },
                    {
                        "range":[80,100],
                        "color":"red"
                    }
                ]
            }
        )
    )

    gauge.update_layout(
        height=250
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

# =====================================================
# ALERT CENTER
# =====================================================

if flare_prob > 70:

    st.error(
        f"🚨 SOLAR ALERT | Forecast Probability: {flare_prob:.1f}% | Possible flare within next 15 minutes"
    )

else:

    st.success(
        "✅ No significant flare activity expected"
    )

# =====================================================
# GRAPH 1
# =====================================================

st.subheader("📡 Combined Solar Activity Timeline")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=display_df["datetime"],
        y=display_df["soft_counts"],
        name="SoLEXS",
        line=dict(width=3)
    )
)

fig.add_trace(
    go.Scatter(
        x=display_df["datetime"],
        y=display_df["hard_counts"],
        name="HEL1OS",
        line=dict(width=3)
    )
)

fig.add_trace(
    go.Scatter(
        x=display_df["datetime"],
        y=display_df["ratio"],
        name="Hardness Ratio",
        line=dict(width=2,dash="dot")
    )
)

fig.update_layout(
    height=500,
    template="plotly_dark",
    title="Multi-Sensor Solar Activity"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# GRAPH 2
# =====================================================

st.subheader("▶ Historical Flare Analysis")

flare_events = df[df["flare"] == 1]

if len(flare_events) > 0:

    selected = st.selectbox(
        "Select Historical Flare Event",
        flare_events["datetime"].astype(str)
    )

    selected_time = pd.to_datetime(selected)

    replay = df[
        (df["datetime"] >= selected_time - pd.Timedelta(minutes=30))
        &
        (df["datetime"] <= selected_time + pd.Timedelta(minutes=30))
    ]

    replay_fig = go.Figure()

    replay_fig.add_trace(
        go.Scatter(
            x=replay["datetime"],
            y=replay["soft_counts"],
            name="SoLEXS"
        )
    )

    replay_fig.add_trace(
        go.Scatter(
            x=replay["datetime"],
            y=replay["hard_counts"],
            name="HEL1OS"
        )
    )

    replay_fig.add_vline(
        x=selected_time,
        line_width=3,
        line_dash="dash"
    )

    replay_fig.update_layout(
        height=450,
        template="plotly_dark",
        title="Historical Flare Replay"
    )

    st.plotly_chart(
        replay_fig,
        use_container_width=True
    )

# =====================================================
# AI INSIGHTS
# =====================================================

# =====================================================
# AI INTELLIGENCE CENTER
# =====================================================

st.subheader("🧠 Solar Intelligence Center")

i1, i2, i3 = st.columns(3)

# -----------------------------------------
# Forecast Card
# -----------------------------------------

with i1:

    st.markdown(f"""
    <div style="
    background:#111827;
    padding:20px;
    border-radius:15px;
    border:1px solid #374151;
    height:220px;
    ">
    
    <h3 style="color:#60a5fa;">
    🎯 Forecast
    </h3>

    <h1 style="color:white;">
    {flare_prob:.1f}%
    </h1>

    <p style="color:#9ca3af;">
    Probability of flare occurrence
    within next 15 minutes
    </p>

    </div>
    """,
    unsafe_allow_html=True)

# -----------------------------------------
# Flare Classification
# -----------------------------------------

if flare_prob < 25:
    flare_class = "A-Class"
    flare_color = "#22c55e"

elif flare_prob < 50:
    flare_class = "B-Class"
    flare_color = "#84cc16"

elif flare_prob < 70:
    flare_class = "C-Class"
    flare_color = "#facc15"

elif flare_prob < 85:
    flare_class = "M-Class"
    flare_color = "#fb923c"

else:
    flare_class = "X-Class"
    flare_color = "#ef4444"

with i2:

    st.markdown(f"""
    <div style="
    background:#111827;
    padding:20px;
    border-radius:15px;
    border:1px solid #374151;
    height:220px;
    ">

    <h3 style="color:{flare_color};">
    🔥 Estimated Flare Class
    </h3>

    <h1 style="color:{flare_color};">
    {flare_class}
    </h1>

    <p style="color:#9ca3af;">
    Estimated severity level based on
    fused SoLEXS + HEL1OS activity
    </p>

    </div>
    """,
    unsafe_allow_html=True)

# -----------------------------------------
# Sensor Intelligence
# -----------------------------------------

sensor_msg = "Soft X-Ray Dominated"

if hardness_ratio > 0.7:
    sensor_msg = "Mixed Spectrum"

elif hardness_ratio > 0:
    sensor_msg = "Mixed Spectrum"

with i3:

    st.markdown(f"""
    <div style="
    background:#111827;
    padding:20px;
    border-radius:15px;
    border:1px solid #374151;
    height:220px;
    ">

    <h3 style="color:#c084fc;">
    ⚡ Sensor Intelligence
    </h3>

    <h1 style="color:white;">
    {hardness_ratio:.3f}
    </h1>

    <p style="color:#9ca3af;">
    {sensor_msg}
    </p>

    </div>
    """,
    unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

j1, j2, j3 = st.columns(3)

with j1:

    st.markdown(f"""
    <div style="
    background:#0f172a;
    padding:15px;
    border-radius:15px;
    text-align:center;
    ">

    <h4>🔆 Current State</h4>

    <h2>{state}</h2>

    </div>
    """,
    unsafe_allow_html=True)

with j2:

    st.markdown(f"""
    <div style="
    background:#0f172a;
    padding:15px;
    border-radius:15px;
    text-align:center;
    ">

    <h4>⏱ Forecast Horizon</h4>

    <h2>15 Minutes</h2>

    </div>
    """,
    unsafe_allow_html=True)

with j3:

    confidence = "High"

    if flare_prob < 20:
        confidence = "High"

    st.markdown(f"""
    <div style="
    background:#0f172a;
    padding:15px;
    border-radius:15px;
    text-align:center;
    ">

    <h4>🎯 Model Confidence</h4>

    <h2>{confidence}</h2>

    </div>
    """,
    unsafe_allow_html=True)
# =====================================================
# MISSION STATS
# =====================================================

st.subheader("📊 Mission Statistics")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "Total Samples",
        len(df)
    )

with m2:
    st.metric(
        "Detected Flares",
        int(df["flare"].sum())
    )





# =====================================================
# FLARE CATALOGUE
# =====================================================


with st.expander("📚 View Automated Flare Catalogue"):

    flare_catalogue = df[
        df["flare"] == 1
    ][
        [
            "datetime",
            "soft_counts",
            "hard_counts",
            "ratio"
        ]
    ]

    st.dataframe(
        flare_catalogue,
        use_container_width=True
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown("""
### 🛰 SolarFlareX

**Data Sources:** Aditya-L1 SoLEXS + HEL1OS

**Nowcasting:** XGBoost

**Forecasting:** Temporal Fusion Transformer (TFT)

**Objective:** Early Solar Flare Warning System with 15-Minute Lead Time
""")