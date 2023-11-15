import requests 
from loguru import logger 
from flask import Flask, request, json ,render_template
from flask_cors import CORS
from config import tokens
from flask_talisman import Talisman

app = Flask(__name__)
CORS(app)
logger.add("flask_app.log", level="DEBUG")

csp = {
    'default-src': '\'self\'',
    'style-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css',  # Tailwind CSS CDN
    ],
    # Add more directives as needed
}

talisman = Talisman(
    app,
    content_security_policy=csp,
    force_https=False,  # Set to True if you want to force HTTPS
)

@app.route('/hello', methods=['POST'])
def hello():
    data = request.get_json()
    if not data: 
        return "telegram bot error",400
    user = data['message']['from'].get('username')
    if user not in tokens:
        return "User not registered . Please register with username and access token",201
    logger.info(json.dumps(data, indent=2))
    url = f"https://api.particle.io/v1/devices/events?access_token={tokens[user]['token']}"
    
    payload = json.dumps({
    "name": tokens[user]['eventname'],
    "data": f"{data['message']['text']}"
    })
    headers = {
   'Content-Type': 'application/json'
     }

    response = requests.request("POST", url, headers=headers, data=payload)
    return "hello", 200

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    user = request.args.get('user')
    token = request.args.get('token')
    eventname = request.args.get('eventname')
    if user and token and eventname:
        tokens[user] = {'token': token , 'eventname': eventname}
        return render_template('successful.html', user=user, token=token, eventname=eventname),200
    return ({"error": "Invalid form data"}), 400

@app.route('/register',methods=['POST'])
def registerPost():
    user = request.form.get('user')
    token = request.form.get('token')
    eventname = request.form.get('eventname')
    if user and token and eventname:
        tokens[user] = {'token': token , 'eventname': eventname}
        return render_template('successful.html', user=user, token=token, eventname=eventname),200
    return ({"error": "Invalid form data"}), 400
   
if __name__ == '__main__':
    app.run()




