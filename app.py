import requests 
from loguru import logger 
from flask import Flask, request, json ,render_template
from flask_cors import CORS
from config import logs
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

@app.route('/<botid>/<accesstoken>/<eventname>',methods=['POST'])
def update(botid,accesstoken,eventname):
    data = request.get_json()
    if data:
        logs.append({'success': 'none' , 'botid': botid ,'eventname': eventname, 'log' : f'Message "{data["message"]["text"]}" from {data["message"]["from"]["username"]}'})
    if data['message']['from']['is_bot']:
        return "ok",200
    url = f"https://api.particle.io/v1/devices/events?access_token={accesstoken}"
    payload = json.dumps({
    "name": eventname,
    "data": f"{data['message']['text']}"
    })
    headers = {
   'Content-Type': 'application/json'
     }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code != 200:
            logs.append({'success' : 'false' , 'botid': botid ,'eventname': eventname , 'log' : f'Invalid Access token : {accesstoken}'})
            return "Invalid access token",400
    except Exception as error:
        logs.append({'success' : 'false' , 'botid': botid ,'eventname': eventname  , 'log' : 'Server Error ! Flask app was unable to send request to particle device'})
        return f'Error in request to particle device', 400
    
    logs.append({'success':'true' ,'botid': botid ,'eventname': eventname , 'log': f'Message "{data["message"]["text"]}" from {data["message"]["from"]["username"]} was sent to particle device with access token {accesstoken}'})
    return 'Data successfully sent to particle device',200


@app.route('/debug')
def debug():
    if logs:
        return render_template('debug.html', logs = logs),200
    return ("Oops ! No logs to display"), 200
  
if __name__ == '__main__':
    app.run()




