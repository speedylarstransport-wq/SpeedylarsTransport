import requests
import os

def enviar_correo(destinatario, asunto, contenido):
    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": os.environ.get("BREVO_API_KEY"),
        "content-type": "application/json"
    }

    data = {
        "sender": {
            "name": "SpeedyLars",
            "email": "speedylarstransport@gmail.com"
        },
        "to": [
            {"email": destinatario}
        ],
        "subject": asunto,
        "htmlContent": contenido
    }

    response = requests.post(url, json=data, headers=headers)

    return response.status_code, response.text