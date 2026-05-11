from openai import OpenAI
import base64
import os
from dotenv import load_dotenv

load_dotenv(override=True)

openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Map Watson voice names (used by the UI) to OpenAI TTS voices
VOICE_MAP = {
    "": "alloy",
    "en-US_MichaelV3Voice": "onyx",
    "en-US_HenryV3Voice": "echo",
    "en-GB_KateV3Voice": "shimmer",
    "en-GB_JamesV3Voice": "fable",
    "en-GB_CharlotteV3Voice": "nova",
    "en-US_LisaV3Voice": "nova",
    "en-US_KevinV3Voice": "echo",
}


def speech_to_text(audio_binary):
    result = openai_client.audio.transcriptions.create(
        model="whisper-1",
        file=("audio.mp3", audio_binary, "audio/mpeg"),
    )
    return result.text


def text_to_speech(text, voice=""):
    tts_voice = VOICE_MAP.get(voice, "alloy")
    response = openai_client.audio.speech.create(
        model="tts-1",
        voice=tts_voice,
        input=text,
        response_format="wav",
    )
    return base64.b64encode(response.content).decode("utf-8")


def openai_process_message(user_message):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful voice assistant. Keep responses concise and conversational."},
            {"role": "user", "content": user_message},
        ],
    )
    return response.choices[0].message.content
