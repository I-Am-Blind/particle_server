import requests 
from flask import Flask, request, json
from flask_cors import CORS




app = Flask(__name__)
CORS(app)

@app.route('/hello', methods=['POST'])
def hello():
    data = request.get_json()
    print(data)
    url = "https://api.particle.io/v1/devices/events?access_token=6150bed281fa3139051d52f44f4cade23b93dbdc"

    payload = json.dumps({
    "name": "telegramUpdate",
    "data": "new update"
    })
    headers = {
   'Content-Type': 'application/json'
     }

    response = requests.request("POST", url, headers=headers, data=payload)
    return "hello", 200

if __name__ == '__main__':
    app.run()




