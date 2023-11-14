import requests 
from loguru import logger 
from flask import Flask, request, json
from flask_cors import CORS




app = Flask(__name__)
CORS(app)
logger.add("flask_app.log", level="DEBUG")

@app.route('/hello', methods=['POST'])
def hello():
    data = request.get_json()
    logger.info(json.dumps(data, indent=2))  # Convert data to JSON format for logging
    url = "https://api.particle.io/v1/devices/events?access_token=6150bed281fa3139051d52f44f4cade23b93dbdc"
    if not data: 
        return "telegram bot error",201
    payload = json.dumps({
    "name": "telegramUpdate",
    "data": f"{data['message']['text']}"
    })
    headers = {
   'Content-Type': 'application/json'
     }

    response = requests.request("POST", url, headers=headers, data=payload)
    return "hello", 200


if __name__ == '__main__':
    app.run()




