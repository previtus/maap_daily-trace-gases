### Fully Automatic Trace Gas Plume Detection - runner for ch4
### Author: Vit Ruzicka, 2026

from pipeline.A_matched_filter.run_wmf_for_scene import ch4_wmf_and_rgb_for_scene
from pipeline.B_ml_segmentation.run_model_on_scene import run_model_on_scene
from pipeline.C_plume_scoring.run_scoring import score_ch4
from timeit import default_timer as timer

def run_for_ch4(tile_ID, results_folder, raws_folder):

    # 1 GET AND COMPUTE DATA (WMF, RGB)
    print("----------------------------------------")
    print("Step 1: getting data, computing WMF, RGB")
    start = timer()
    ch4_wmf_and_rgb_for_scene(tile_ID, raws_folder, results_folder)
    end = timer()
    time = (end - start)
    print("^^^ Step 1 took "+str(time)+"s ("+str(time/60.0)+"min)")
    # 54.571396014000015s (0.9095232669000003min)

    # 2 MODEL PREDICTION
    print("----------------------------------------")
    print("Step 2: model prediction")
    start = timer()
    run_model_on_scene(tile_ID, results_folder, use_ensemble = True)
    end = timer()
    time = (end - start)
    print("^^^ Step 2 took "+str(time)+"s ("+str(time/60.0)+"min)")
    # 20.015326303999984s (0.33358877173333307min)

    # 3 SCORE PREDICTIONS
    print("----------------------------------------")
    print("Step 3: scoring predictions")
    start = timer()
    saved_scored_vectors_path = score_ch4(tile_ID, results_folder, raws_folder, use_ensemble = True)
    end = timer()
    time = (end - start)
    print("^^^ Step 3 took "+str(time)+"s ("+str(time/60.0)+"min)")
    # 91.44824060000002s (1.5241373433333336min)

    return saved_scored_vectors_path


