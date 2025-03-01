import requests

def fetch_html(url, filename=None, save=True):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error downloading html: {response.status_code}")

    return response.text