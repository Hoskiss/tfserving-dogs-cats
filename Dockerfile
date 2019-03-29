# Using the official tensorflow serving image from docker hub as base image
FROM tensorflow/serving

# nginx to rever proxy if we use sagemaker, would not configure it for now
RUN apt-get update && apt-get install -y --no-install-recommends nginx git

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv

COPY requirements.txt requirements.txt

RUN python3.6 -m pip install pip --upgrade

RUN python3.6 -m pip install -r requirements.txt

# Copy our model folder to the container
COPY tfserving_dogs_cats_models /tfserving_dogs_cats_models

COPY flask_serving_app.py flask_serving_app.py

COPY docker_service.sh docker_service.sh

# rewrite the ENTRYPOINT in tensorflow/serving dockerfile
ENTRYPOINT ["/bin/bash", "./docker_service.sh"]
