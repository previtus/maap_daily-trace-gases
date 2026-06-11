#!/bin/bash

BASEDIR=$( cd "$(dirname "$0")" ; pwd -P)

# prepare output directory
OUTPUTDIR="${PWD}/output"
mkdir -p ${OUTPUTDIR}

# Read the positional argument as defined in the algorithm registration here
emit_scene_name=$1
gas=$2

export PYTHONPATH="$BASEDIR/daily-trace-gases:$PYTHONPATH"
export GDAL_DATA=/srv/conda/envs/notebook/share/gdal

echo "daily-trace-gases codebase run!"
python ${BASEDIR}/daily-trace-gases/detect_trace_gas.py -tile $1 -gas $2 -basedir ${BASEDIR}/daily-trace-gases/ -results_folder ${OUTPUTDIR}

echo "---"
echo "ls ${OUTPUTDIR}/*"
ls ${OUTPUTDIR}/*
echo "---"
