python ./export_model.py
docker build -t tf-serving-dogs-cats-predict .
docker run --rm -p 8080:8080 tf-serving-dogs-cats-predict