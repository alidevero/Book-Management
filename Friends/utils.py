import requests # type: ignore

def send_webhook_notification(url, data):
    """Send webhook notification to external services"""
    try:
        response = requests.post(url, json=data, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Webhook Error: {e}")
