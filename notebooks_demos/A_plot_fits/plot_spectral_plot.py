from daily_trace_gases.utils.vec_utils import vec_load
import pylab as plt

def signal_ratio_target_plot(ratio, fit_sig, wl, polyn, ax = None):
    if ax is None:
        fig, axes = plt.subplots(1, 1, figsize=(6 * 1.4, 3 * 1.4), constrained_layout=True, squeeze=False)
        axes = axes.flatten()
        ax = axes[0]

    ratio_p_ = ratio.copy() / polyn
    fit_sig_p_ = fit_sig.copy() / polyn

    ax.plot(wl, ratio_p_, label='Measurement')
    ax.plot(wl, fit_sig_p_, label='Modelled target')
    ax.set_xlabel('Wavelength')
    ax.set_ylabel('Transmittance')

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels,
               loc='upper right',
               # bbox_to_anchor=(0, 1),
               fontsize=8)

    return ax

def plots_for_vector(vector_path):
    df = vec_load(vector_path)
    print(df)

    for idx, row in df.iterrows():
        print(row.keys())
        print(row)

        shapely_vector = row["geometry"]
        c = shapely_vector.centroid
        lon = c.x
        lat = c.y

        ax = signal_ratio_target_plot(row["ratio"], row["fit_sig"], row["wl"], row["polyn"])
        plt.show()

        # break


if __name__ == '__main__':
    vector_path = "/Users/ruzicka/Downloads/DATA/_intermediate_folder/outputs_tmp/EMIT_L1B_RAD_001_20260102T143123_2600209_005/prediction_ensemble_scored.geojson"
    plots_for_vector(vector_path)