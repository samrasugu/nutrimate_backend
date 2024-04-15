from flask import Flask, request, jsonify
from chat import BotClient

app = Flask(__name__)

# debug mode
app.config['DEBUG'] = True

@app.route('/api', methods=['POST'])
def api():
    data = request.get_json()
    # return jsonify(data)
    return "Hello, World!"

@app.route('/chat', methods=['POST'])
def recognize_text():
    
    message = request.get_json()['message']
    
    response = BotClient().recognize_text(message=message)
    
    return jsonify(response)


if __name__ == '__main__':
    app.run()