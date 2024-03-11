from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def get_transcript_from_whisper(audio_file_path):
    """
    Transcribe audio file using the OpenAI API with the "whisper-1" model.

    Args:
        audio_file_path (str): The path to the audio file.

    Returns:
        dict or None: The transcription data from the API response, or None if an error occurs.
    """
    try:
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        openai_client = OpenAI(api_key = OPENAI_API_KEY)
        with open(audio_file_path, "rb") as audio_file:
            transcription = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            return transcription
    except Exception as e:
        print(f"Error: {e}")
        return None
