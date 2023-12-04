from flask import Flask, render_template, request, jsonify
import requests

RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    user_message = request.json.get('message')
    print("User Message:", user_message)

    if user_message:
        # Send user message to Rasa and get bot's response
        rasa_response = requests.post(RASA_API_URL, json={'message': user_message})
        
        if rasa_response.status_code == 200:
            rasa_response_json = rasa_response.json()
            print("Rasa Response:", rasa_response_json)
            
            if rasa_response_json:
                bot_response = rasa_response_json[0]['text']
            else:
                bot_response = "Sorry, I didn't understand that."
        else:
            bot_response = "Failed to fetch a response from Rasa."

    else:
        bot_response = "No message received."

    return jsonify({'response': bot_response})

if __name__ == "__main__":
    app.run(debug=True, port=3001)