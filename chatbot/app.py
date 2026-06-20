import json
import random
from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# 1. Load predefined commercial input patterns
with open('intents.json', 'r') as file:
    data = json.load(file)

all_patterns = []
pattern_to_intent = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        all_patterns.append(pattern.lower())
        pattern_to_intent.append(intent)

# 2. Train the TF-IDF Vectorizer for instant-response pattern matching
vectorizer = TfidfVectorizer()
vectorizer.fit(all_patterns)

def get_bot_response(user_text):
    user_text = user_text.lower()
    
    # Transform input text to match against training vectors
    user_vector = vectorizer.transform([user_text])
    pattern_vectors = vectorizer.transform(all_patterns)
    
    # Calculate text similarity metrics
    similarities = cosine_similarity(user_vector, pattern_vectors).flatten()
    max_idx = similarities.argmax()
    
    # Accuracy safety threshold (0.2 minimum match score)
    if similarities[max_idx] < 0.2:
        return "I'm sorry, I couldn't quite understand that. Could you please rephrase your query?"
    
    matched_intent = pattern_to_intent[max_idx]
    return random.choice(matched_intent['responses'])

# 3. Web Interface Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"response": "Please enter a valid message."}), 400
    
    bot_reply = get_bot_response(user_message)
    return jsonify({"response": bot_reply})

if __name__ == '__main__':
    # Starts local testing host on port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)