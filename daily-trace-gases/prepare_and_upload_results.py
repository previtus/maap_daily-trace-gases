### Fully Automatic Trace Gas Plume Detection
### Author: Vit Ruzicka, 2026

import os.path
from timeit import default_timer as timer
import argparse
from utils.rio_utils import mkdir
from utils.paths import set_basedir
from utils.paths import codebase_folder, models_storage
import os
import time
import random
from huggingface_hub import HfApi, CommitOperationAdd
from huggingface_hub.utils import RepositoryNotFoundError
from maap.maap import MAAP
import os
import os.path
maap = MAAP()
os.environ["HF_TOKEN"] = maap.secrets.get_secret("HF_TOKEN")

parser = argparse.ArgumentParser(description='Codebase: Results uploader.')
parser.add_argument('-gas', help='Which trace gas? (options: ch4, nh3, no2 and co)', default='ch4')
parser.add_argument('-tile', help='Which EMIT tile to run? (e.g. EMIT_L1B_RAD_001_20260102T143123_2600209_005)', default='EMIT_L1B_RAD_001_20260102T143123_2600209_005')
parser.add_argument('-results_folder', help='Folder to save results to', default='./run_data/results')
parser.add_argument('-basedir', help='Location of this code', default='daily-trace-gases/')

def hf_upload_with_retry(files_to_upload, target_folder, gas, tile_ID, hf_repo, max_retries = 10):
    api = HfApi()

    # Define the two files this specific job needs to upload
    operations = []
    for file_path in files_to_upload:
        file_name = file_path.split("/")[-1]
        operations.append(
            CommitOperationAdd(
                path_in_repo=target_folder+"/"+file_name,
                path_or_fileobj=file_path
            )
        )

    # Retry loop to handle repository lock competition from other many (N > 40) jobs
    for attempt in range(max_retries):
        try:
            api.create_commit(
                repo_id=hf_repo,
                operations=operations,
                commit_message=f"Upload results from EMIT scene {tile_ID} and gas {gas}",
                repo_type="dataset"
            )
            print(f"Success: Job uploaded successfully.")
            break  # Exit loop on success

        except Exception as e:
            print(e)

            if attempt == max_retries - 1:
                print(f"Error: Job failed after {max_retries} attempts.")
                raise e

            # Generates a random wait time (e.g., between 5 and 30 seconds)
            # This prevents all 40 jobs from retrying at the exact same millisecond
            wait_time = random.uniform(5, 30) + (attempt * 10)
            print(f"Repo locked by another job. Retrying in {wait_time:.2f} seconds...")
            time.sleep(wait_time)

def tile_name_to_date(tile_name = "EMIT_L1B_RAD_001_20260525T035831_2614503_008"):
    date_str = tile_name.split("_")[4].split("T")[0]
    # 20260525
    return date_str[0:4] + "-" + date_str[4:6] + "-" + date_str[6:]

if __name__ == '__main__':
    start = timer()

    args = parser.parse_args()

    # Paths and args:
    tile_ID = args.tile
    gas = args.gas
    basedir = args.basedir
    set_basedir(basedir)
    results_folder = args.results_folder

    # Rename and upload results
    files_to_upload = []
    mf_product = ""
    if gas == "ch4":
        mf_product = "ch4-wmf.tif"
    else:
        mf_product = gas+"-cmf.tif"

    raster_path_ = os.path.join(results_folder, tile_ID, mf_product)
    raster_path = os.path.join(results_folder, tile_ID, tile_ID+".tif")
    vector_path_ = os.path.join(results_folder, tile_ID, "prediction_ensemble_scored.geojson")
    vector_path = os.path.join(results_folder, tile_ID, tile_ID+".geojson")

    os.rename(raster_path_, raster_path)
    os.rename(vector_path_, vector_path)

    files_to_upload.append(raster_path)
    files_to_upload.append(vector_path)

    # HF repo: https://huggingface.co/datasets/previtus/jpl_trace_gases_archive
    hf_repo = "previtus/jpl_trace_gases_archive"

    target_folder = gas+"/"+tile_name_to_date(tile_ID)

    print("Will try uploading these files: ", files_to_upload, "into", target_folder)

    hf_upload_with_retry(files_to_upload, target_folder, gas, tile_ID, hf_repo, max_retries = 10)

    end = timer()
    time = (end - start)
    print("Upload itself took "+str(time)+"s ("+str(time/60.0)+"min)")
