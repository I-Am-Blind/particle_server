import requests 
from loguru import logger 
from flask import Flask, request, json
from flask_cors import CORS
from config import tokens




app = Flask(__name__)
CORS(app)
logger.add("flask_app.log", level="DEBUG")

@app.route('/hello', methods=['POST'])
def hello():
    data = request.get_json()
    if not data: 
        return "telegram bot error",400
    user = data['message']['from'].get('username')
    if user not in tokens:
        return "User not registered . Please register with username and access token",201
    logger.info(json.dumps(data, indent=2))
    url = f"https://api.particle.io/v1/devices/events?access_token={tokens[user]}"
    
    payload = json.dumps({
    "name": "telegramUpdate",
    "data": f"{data['message']['text']}"
    })
    headers = {
   'Content-Type': 'application/json'
     }

    response = requests.request("POST", url, headers=headers, data=payload)
    return "hello", 200

@app.route('/register',)
def register():
    user = request.args.get('user')
    token = request.args.get('token')
    if user and token:
        tokens[user] = token
        print(tokens)
        return f"Successfully registered user  {user} with access token {token}",200
    return "Invalid query parameters",201
   
if __name__ == '__main__':
    app.run()




