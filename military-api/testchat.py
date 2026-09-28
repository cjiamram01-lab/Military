
import requests

API_KEY = "sk-4339e071f1cf41af885bc9db84c74a25"
API_URL = "https://api.deepseek.com/v1/chat/completions"  # Example endpoint

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "deepseek-chat",  # Replace with the correct model name
    "messages": [
        {"role": "user", "content": "Explain quantum computing in 50 words."}
    ],
    "temperature": 0.7,
    "max_tokens": 150
}

response = requests.post(API_URL, headers=headers, json=data)

if response.status_code == 200:
    result = response.json()
    print(result["choices"][0]["message"]["content"])
else:
    print(f"Error: {response.status_code}, {response.text}")
