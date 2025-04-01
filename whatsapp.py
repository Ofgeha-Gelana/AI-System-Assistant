


import requests

def send_whatsapp_message(phone_number, message):
    ACCESS_TOKEN = "ytzsehRrGwMjBqP1W2DsrZ7VCojtIZUzyCoR6Wb67dcee8fe"  # Replace with your WhatsApp Cloud API token
    PHONE_NUMBER_ID = "+251935070773"  # Replace with your Phone Number ID
    API_URL = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "testing",
        "text": {"body": message}
    }

    response = requests.post(API_URL, json=payload, headers=headers)
    return response.json()

# Example Usage:
response = send_whatsapp_message("1234567890", "Hello from WhatsApp API!")
print(response)
