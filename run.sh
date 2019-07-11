python ./export_model.py
# docker build --no-cache -t tf-serving-dogs-cats .
docker build -t tf-serving-dogs-cats .
docker rmi $(docker images | grep '^<none>' | awk '{print $3}')
docker run --rm -p 8081:8081 --name tf-serving-dogs-cats-env tf-serving-dogs-cats