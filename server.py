import base64
import json
from flask import Flask, render_template, request
from worker import speech_to_text, text_to_speech, openai_process_message
from flask_cors import CORS
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    text = speech_to_text(request.data)
    response = app.response_class(
        response=json.dumps({"text": text}),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/process-message', methods=['POST'])
def process_prompt_route():
    user_message = request.json.get("userMessage")
    voice = request.json.get("voice", "")
    openai_response_text = openai_process_message(user_message)
    openai_response_speech = text_to_speech(openai_response_text, voice)
    response = app.response_class(
        response=json.dumps({"openaiResponseText": openai_response_text, "openaiResponseSpeech": openai_response_speech}),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0')
