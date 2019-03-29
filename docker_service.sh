#!/bin/bash

# https://docs.docker.com/config/containers/multi-service_container/
# turn on bash's job control
set -m

# Start the model server process and put it in the background
tensorflow_model_server --rest_api_port=8501 \
    --model_name=tfserving_dogs_cats_models \
    --model_base_path=/tfserving_dogs_cats_models &

# Start the flask process
python3 ./flask_serving_app.py
