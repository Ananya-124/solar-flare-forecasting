from astropy.io import fits

path = r"data/raw/hel1os/HLS_20240708_120001_43190sec_lev1_V111/cdte/lightcurve_cdte1.fits"

with fits.open(path) as hdul:

    for i in range(len(hdul)):

        try:
            data = hdul[i].data

            print("\nHDU:", i)

            if data is not None:
                print("Rows:", len(data))
                print(data[:3])

        except Exception as e:
            print(i, e)