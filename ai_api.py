import requests

API_TOKEN = ""

api_url = "https://api-inference.huggingface.co/models/t5-small"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

data = {"inputs": "Say hello"}

response = requests.post(api_url, headers=headers, json=data)
if response.status_code == 200:
    print(response.json()[0]["generated_text"])
else:
    print("Error:", response.status_code, response.text)
