import httpx

def fetch_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        with httpx.Client(verify=False, timeout=20) as client:  # 20 sekund timeoutu
            response = client.get(url)
            response.raise_for_status()  # Wymusi zgłoszenie błędu HTTP, jeśli wystąpi
            return response.text
    except httpx.HTTPStatusError as e:
        print(f"Error: HTTPStatusError: {e.response.status_code} - {e.response.text}")
    except httpx.TimeoutException:
        print("Error: TimeoutException")
    except httpx.RequestError as e:
        print(f"Error: RequestError: {e}")

    return None
