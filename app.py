from flask import Flask, request, jsonify
from chat import BotClient
from dotenv import load_dotenv

app = Flask(__name__)

# debug mode
app.config['DEBUG'] = True

@app.route('/', methods=['GET'])
def api():
    return "Hello, World!"

@app.route('/chat', methods=['POST'])
def recognize_text():
    
    message = request.get_json()['message']
    
    response = BotClient().recognize_text(message=message)
    
    return jsonify(response)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)