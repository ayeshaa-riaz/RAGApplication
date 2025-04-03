import requests

api_key = "G7cjgYR8DnsSVGCbo8j256hHqMtN2gK5Ro9emebs"
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

data = {
    "texts": ["test sentence"], 
    "model": "embed-english-v3.0", 
    "input_type": "search_document"  # or "search_query" depending on use case
}

response = requests.post("https://api.cohere.com/v1/embed", json=data, headers=headers)
print(response.json())  # Should return an embedding if valid
