import os
import json
import base64
import requests

server_endpoint = 'http://localhost:8080/invocations'
img_paths = [
    os.path.join(os.getcwd(), "testdata", "dog.jpg")
]

# Load and Base64 encode images
data_samples = []
for path in img_paths:
    with open(path, 'rb') as image_file:
        b64_image = base64.b64encode(image_file.read())
        data_samples.append({'image_bytes': {'b64': b64_image.decode('utf-8')}})

# Create payload request
payload = json.dumps({"instances": data_samples})

# Send prediction request
r = requests.post(server_endpoint, data=payload)
print(json.loads(r.content))