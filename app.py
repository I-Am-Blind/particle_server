from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/hello', methods=['POST'])
def hello():
    data = request.get_json()

    if 'name' in data and 'message' in data:
        name = data['name']
        message = data['message']
        return jsonify({'response': f'Hello, {name}! You said: {message}'}), 200
    else:
        return jsonify({'error': 'Invalid request. Please provide "name" and "message" in the request body.'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
