# get_ngrok_url.py
import requests
import time

def get_ngrok_url():
    retries = 0
    while retries < 10:
        try:
            print("Attempting to fetch ngrok URL...")
            response = requests.get("http://ngrok:4040/api/tunnels")  # Use `ngrok` service name directly
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            return data["tunnels"][0]["public_url"]
        except requests.exceptions.RequestException:
            retries += 1
            time.sleep(5)  # Wait for 5 seconds before retrying
    return "Error: Could not connect to ngrok API"

if __name__ == "__main__":
    url = get_ngrok_url()
    print("Ngrok URL:", url)
