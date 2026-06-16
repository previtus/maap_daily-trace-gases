import rasterio
import numpy as np

def compress_mf_tif(input_path, output_path):
    # estimated: from about 20MB to about 3MB?

    # Compression for visualisation purposes - keeps the way how this file would open in QGIS for visualisation
    # but uses the min-max from the data
    # For any purpose other than visualisation we'd need to rerun this!

    # # min max either from data, or we could ...
    # min_max_for_gas = {
    #     "ch4": [0, 0.3],
    #     "nh3": [0, 15_000],
    #     "no2": [0, 70_000],
    #     "co": [0, 12_000],
    # }

    with rasterio.open(input_path) as src:
        float_data = src.read(1)
        meta = src.meta.copy()

        # mask no data to 0 (important, before the min/max)
        float_data = np.where(float_data == meta["nodata"], 0.0, float_data)

        # rescale to 0-255
        min_val, max_val = np.nanmin(float_data), np.nanmax(float_data)
        if max_val == min_val: max_val += 1

        rescaled = 255 * (float_data - min_val) / (max_val - min_val)
        uint8_data = np.nan_to_num(rescaled).astype(np.uint8)

        # then still set those to 0 (otherwise they were
        uint8_data = np.where(float_data == meta["nodata"], 0, uint8_data).astype(np.uint8)

        # set compression
        meta.update(
            dtype=rasterio.uint8,
            count=1,
            nodata=0,
            compress="deflate",
            predictor=2
        )

        with rasterio.open(output_path, "w", **meta) as dst:
            dst.write(uint8_data, 1)
