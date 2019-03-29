python ./export_model.py
docker build -t tf-serving-dogs-cats-predict .
docker run --rm -p 8081:8081 tf-serving-dogs-cats-predict