# Using the official tensorflow serving image from docker hub as base image
FROM tensorflow/serving

# Installing NGINX, used to rever proxy the predictions from SageMaker to TF Serving
RUN apt-get update && apt-get install -y --no-install-recommends nginx git

# Copy our model folder to the container
COPY tfserving_dogs_cats_models /tfserving_dogs_cats_models

# Copy NGINX configuration to the container
COPY nginx.conf /etc/nginx/nginx.conf

# starts NGINX and TF serving pointing to our model
ENTRYPOINT service nginx start | tensorflow_model_server --rest_api_port=8501 \
 --model_name=tfserving_dogs_cats_models \
 --model_base_path=/tfserving_dogs_cats_models