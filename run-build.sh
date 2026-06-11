#!/bin/bash

basedir=$( cd "$(dirname "$0")" ; pwd -P )

pip install -r ${basedir}/requirements.txt

pip install pyogrio
pip install torch==2.12.0 torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -U segmentation-models-pytorch
pip install -U "huggingface_hub[cli]"

hf download previtus/JPL_TRACE_GASES_MODELS --local-dir ${basedir}/daily-trace-gases/models/JPL_TRACE_GASES_MODELS
pip install maap-py
pip install gdown
pip install fiona
