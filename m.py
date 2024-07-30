"""
A simple web-based chat interface for the Google AI Python SDK

Requirements:
- pip install google-generativeai flask

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os
import json
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key="AIzaSyD3mBxEx5d5CA9YLOkjHIQ6sQiicTG3KsA")

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You are an autocompletion AI, you complete the text given to you, such as:\n\nMaths:\nUser: 2+23(23-2)\nYou: \n= 2+23(21)\n= 2+483\n= 485\n\nQuestions:\nUser: The french revultion happened on \nYou: 1787\n\nIf there is a error with the input, respond like this:\n(!) Error: <error message>",
)

HISTORY_FILE = "chat_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

history = load_history()

chat_session = model.start_chat(history=history)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    response = chat_session.send_message(user_input)
    history.append({"role": "user", "parts": [user_input]})
    history.append({"role": "model", "parts": [response.text]})
    save_history(history)
    return jsonify({"response": response.text})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)