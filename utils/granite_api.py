import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

API_KEY = os.getenv("IBM_API_KEY")
REGION = os.getenv("IBM_REGION")
PROJECT_ID = os.getenv("IBM_PROJECT_ID")

def get_iam_token(api_key):
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "apikey": api_key,
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
    }
    response = requests.post(url, headers=headers, data=data)
    json_resp = response.json()
    if "access_token" in json_resp:
        return json_resp["access_token"]
    else:
        raise Exception(f"Failed to get IAM token: {json_resp}")


def query_granite(prompt):
    token = get_iam_token(API_KEY)
    url = f"https://{REGION}.ml.cloud.ibm.com/ml/v1/text/generation?version=2024-05-10"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
               "model_id": "ibm/granite-13b-instruct-v2",  # 👈 use this
               "input": prompt,
               "project_id": PROJECT_ID,
               "parameters": {
               "decoding_method": "greedy",
               "max_new_tokens": 200
    }
}

    

    response = requests.post(url, headers=headers, json=payload)

    try:
        response_data = response.json()
        print("🪵 Full API Response:", response_data)  # 👈 Debug output
        if "results" in response_data and len(response_data["results"]) > 0:
            generated_text = response_data["results"][0].get("generated_text")
            return generated_text if generated_text else "⚠️ No response text generated."
        else:
            return "⚠️ No results found in response."
    except Exception as e:
        return f"❌ Error parsing response: {e}"
