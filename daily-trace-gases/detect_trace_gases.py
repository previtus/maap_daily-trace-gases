### Fully Automatic Trace Gas Plume Detection
### Author: Vit Ruzicka, 2026

import os.path
from timeit import default_timer as timer
import argparse
from utils.paths import set_basedir
from detect_trace_gas import detect_trace_gas

parser = argparse.ArgumentParser(description='Codebase: Fully Automatic Trace Gas Plume Detection.')
parser.add_argument('-gases', help='Which trace gases? Multiple are possible, separated by comma (options: ch4, nh3, no2 and co)', default='ch4,nh3,no2,co')
parser.add_argument('-tile', help='Which EMIT tile to run? (e.g. EMIT_L1B_RAD_001_20260102T143123_2600209_005)', default='EMIT_L1B_RAD_001_20260102T143123_2600209_005')
parser.add_argument('-raws_folder', help='Folder to store intermediate files', default='./run_data/intermediates_folder')
parser.add_argument('-results_folder', help='Folder to save results to', default='./run_data/results')
parser.add_argument('-basedir', help='Location of this code', default='daily-trace-gases/')

if __name__ == '__main__':
    args = parser.parse_args()
    start = timer()

    tile_ID = args.tile
    gases = args.gases

    basedir = args.basedir

    results_folder = args.results_folder
    raws_folder = args.raws_folder

    # ### <LOCAL OVERRIDE>
    # basedir = "/Users/ruzicka/Downloads/CODES/maap_daily-trace-gases/daily-trace-gases"
    # results_folder = "/Users/ruzicka/Downloads/DATA/_intermediate_folder/outputs_tmp"
    # raws_folder = "/Users/ruzicka/Downloads/DATA/_intermediate_folder"
    # gases = "ch4"
    # tile_ID = "EMIT_L1B_RAD_001_20260102T143123_2600209_005"
    # set_basedir(basedir)
    # ### </LOCAL OVERRIDE>

    if "," in gases:
        gases_list = gases.split(",")
        for gas in gases_list:
            start = timer()
            detect_trace_gas(gas, tile_ID, results_folder, raws_folder)
            end = timer()
            time = (end - start)
            print("Gas",gas,"took " + str(time) + "s (" + str(time / 60.0) + "min)")

    else:
        # or it's just a single one
        detect_trace_gas(gases, tile_ID, results_folder, raws_folder)

    end = timer()
    time = (end - start)
    print("Full run took "+str(time)+"s ("+str(time/60.0)+"min)")
    # This run took 106.00505466899995s (1.766750911149999min)