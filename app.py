from flask import Flask, render_template, request, jsonify
import json
import random

app = Flask(__name__)

with open('health_data.json', 'r', encoding='utf-8') as file:
    health_data = json.load(file).get('keywords', {})


def get_response(user_input):
    """
    Checks the user's input for keywords and returns the appropriate response
    from the health data dictionary or a basic greeting.
    """
    user_input_lower = user_input.lower()

    
    greetings = ['hello', 'hi', 'hey', 'namaste', 'ନମସ୍କାର']
    if any(word in user_input_lower for word in greetings):
        return random.choice(['Hello! How can I help you today?', 'Hi there!', 'Greetings! What can I do for you?', 'Hello! I am a health assistant.'])

  
    keywords_map = {
        'dengue': 'dengue_symptoms',
        'fever': 'dengue_symptoms',
        'malaria': 'malaria_symptoms',
        'vaccine': 'vaccine_schedule',
        'prevention': 'dengue_prevention',
        'symptoms': 'dengue_symptoms',
        'ମ୍ୟାଲେରିଆ': 'malaria_symptoms',
        'ନିବାରଣ': 'dengue_prevention',
        'ଟୀକାକରଣ': 'vaccine_schedule',
        'ଲକ୍ଷଣ': 'dengue_symptoms'
    }

    for keyword, key in keywords_map.items():
        if keyword in user_input_lower:
            
            odia_keywords = ['ମ୍ୟାଲେରିଆ', 'ନିବାରଣ', 'ଟୀକାକରଣ', 'ଲକ୍ଷଣ', 'ନମସ୍କାର']
            is_odia = any(word in user_input_lower for word in odia_keywords)
            
            if is_odia:
                
                return health_data.get(key, {}).get('hi', health_data.get(key, {}).get('en', 'Sorry, I do not have information in Odia for that.'))
            else:
                return health_data.get(key, {}).get('en', 'Sorry, I do not have information on that topic.')

    
    return "Sorry, I can't help with that query. Please try asking about 'dengue', 'malaria', or 'vaccine'."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def chatbot_response():
    user_message = request.json.get('message')
    response = get_response(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)