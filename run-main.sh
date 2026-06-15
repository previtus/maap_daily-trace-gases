#!/bin/bash

SECONDS=0

BASEDIR=$( cd "$(dirname "$0")" ; pwd -P)

# prepare output directory
OUTPUTDIR="${PWD}/output"
mkdir -p ${OUTPUTDIR}

# Read the positional argument as defined in the algorithm registration here
emit_scene_name=$1
gas=$2

export PYTHONPATH="$BASEDIR/daily-trace-gases:$PYTHONPATH"
export GDAL_DATA=/srv/conda/envs/notebook/share/gdal

duration=$SECONDS
echo "Init before code execution from bash start took - $((duration / 60)) minutes and $((duration % 60)) seconds elapsed."

echo "daily-trace-gases codebase run!"
python ${BASEDIR}/daily-trace-gases/detect_trace_gases.py -tile $1 -gas $2 -basedir ${BASEDIR}/daily-trace-gases/ -results_folder ${OUTPUTDIR}

echo "Checkpoint after execution, from bash start took - $((duration / 60)) minutes and $((duration % 60)) seconds elapsed."

echo "upload command run!"
python ${BASEDIR}/daily-trace-gases/prepare_and_upload_results.py -tile $1 -gas $2 -basedir ${BASEDIR}/daily-trace-gases/ -results_folder ${OUTPUTDIR}

echo "Checkpoint after upload, from bash start took - $((duration / 60)) minutes and $((duration % 60)) seconds elapsed."

echo "---"
echo "ls ${OUTPUTDIR}/*"
ls ${OUTPUTDIR}/*
echo "---"
