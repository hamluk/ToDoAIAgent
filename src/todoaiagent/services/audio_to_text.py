import speech_recognition as sr
from speech_recognition import google

def audio_to_text(audio_file_path: str) -> str:
    """
    Convert audio file to text using a speech-to-text model.

    Args:
        audio_file_path (str): Path to the audio file.

    Returns:
        str: Transcribed text from the audio.
    """
    r = sr.Recognizer()

    with sr.AudioFile(audio_file_path) as source:
        audio_data = r.record(source)
        text = google.recognize_legacy(recognizer=r ,audio_data=audio_data)

        return text
