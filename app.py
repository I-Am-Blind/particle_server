import requests 
from loguru import logger 
from flask import Flask, request, json ,render_template ,redirect
from flask_cors import CORS
from config import logs,all_data
from flask_talisman import Talisman

app = Flask(__name__)
CORS(app)
logger.add("flask_app.log", level="DEBUG")

csp = {
    'default-src': '\'self\'',
    'style-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css',
    ],
}

talisman = Talisman(
    app,
    content_security_policy=csp,
    force_https=False, 
)

@app.route('/register',methods = ['GET'])
def login():
    return render_template('login.html'),200

@app.route('/register', methods=['POST'])
def registerPost():
    team_name = request.form.get('team_name')
    bot_id = request.form.get('bot_id')
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')
    eventname = request.form.get('eventname')

    if client_id:
        auth_url = "https://api.particle.io/oauth/token"
        payload = f'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.request("POST", auth_url, headers=headers, data=payload)
        response_data = response.json()
        if response.status_code == 200:
           webhook_url = f"https://api.telegram.org/bot{bot_id}/setWebhook?url=https://particle-api-d8i53.ondigitalocean.app/{bot_id}/{response_data.get('access_token')}/{eventname}/{team_name}"
           response = requests.request("POST", webhook_url, headers={}, data={})
           if response.status_code == 200:
               all_data[bot_id] = {'bot_id': bot_id ,'access_token':response_data.get('access_token'),'event_name':eventname , 'team_name': team_name}
               return render_template('successful.html', data=all_data[bot_id])
           return render_template('error.html',error = "Telegram Bot setWebhook API Error!" ,sub = f"Please verify Telegram Bot ID : {bot_id}"),200
        return render_template('error.html',error = "Particle AuthToken Generation error!" , sub = f"Please verify the following :<br>Client ID : {client_id}<br>Client Secret : {client_secret}"),200       
    return render_template('error.html',error = "Invalid Entries! Please try again" , sub = ""),200     

    
@app.route('/<botid>/<accesstoken>/<eventname>/<teamname>',methods=['POST'])
def update(botid,accesstoken,eventname,teamname):
    data = request.get_json()
    if not data:
        logs.append({'success': 'false' ,'team_name' : teamname ,'botid': botid ,'eventname': eventname, 'log' : f'No data recieved from telegram webhook'})
        return "Error" ,400
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
            logs.append({'success' : 'false','team_name' : teamname , 'botid': botid ,'eventname': eventname , 'log' : f'Invalid Access token : {accesstoken}'})
            return "Invalid access token",400
    except Exception as error:
        logs.append({'success' : 'false','team_name' : teamname , 'botid': botid ,'eventname': eventname  , 'log' : 'Server Error ! Flask app was unable to send request to particle device'})
        return f'Error in request to particle device', 400
    
    logs.append({'success':'true','team_name' : teamname ,'botid': botid ,'eventname': eventname , 'log': f'Message "{data["message"]["text"]}"  was sent to particle device with access token {accesstoken}'})
    return 'Data successfully sent to particle device',200


@app.route('/deleteWebhook/<botid>')
def deleteWebhoo(botid):
    if botid in all_data:
        del all_data[botid]
    url = f"https://api.telegram.org/bot{botid}/deleteWebhook"
    response = requests.request("POST", url, headers={}, data={})
    return render_template('error.html',error = response.json()['description'] ,sub = response.status_code )

@app.route('/debug/logs')
def debug():
    if logs:
        return render_template('debug.html', logs = logs),200
    return render_template('error.html',error = "Oops ! No Logs yet " , sub = "" ),200

@app.route('/debug/admin')
def admin():
    if all_data:
        return render_template('admin.html', data = all_data),200
    return render_template('error.html',error = "Oops ! No Registrations yet " , sub = ""),200

@app.route('/debug/delete/logs')
def delete():
    logs.clear()
    return redirect('/debug/logs')

if __name__ == '__main__':
    app.run()




