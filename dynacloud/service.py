import logging
from flask import abort
from werkzeug.datastructures import FileStorage
from .config import GOOGLE_API_KEY, APP_AUTH_TOKEN
from .exceptions import *
from google.cloud import vision
from google.cloud import texttospeech
from google.api_core.client_options import ClientOptions


clientOptions = ClientOptions(api_key=GOOGLE_API_KEY)


def parse_token_from_auth_header(auth_header) -> str | None:
    try:
        if isinstance(auth_header, str):
            auth_token = auth_header.strip().split(" ")[-1]
            logging.info(f'parse_token_from_auth_header;SUCCESS;AUTH_HEADER;{auth_header};TOKEN;{auth_token}')
            return auth_token
        else:
            logging.info(f'parse_token_from_auth_header;None;AUTH_HEADER;{auth_header};TOKEN;{None}')
            return None
    except BaseException as err:
        logging.warning(f'parse_token_from_auth_header;error;{err}')
        return None


def check_auth_token_is_valid(token: str | None) -> bool:
    if token is None or token != APP_AUTH_TOKEN:
        logging.warning(f'check_auth_token_is_valid;INVALID;TOKEN;{token}')
        abort(401, "The server could not verify that you are authorized to access the URL requested.")

    logging.info(f'check_auth_token_is_valid;VALID;TOKEN;{token}')
    return True


def detect_text(file: FileStorage) -> list:
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient(client_options=clientOptions)

    image = vision.Image(content=file.read())
    response = client.text_detection(image=image)

    if response.error.message:
        raise CustomException(response.error.message, 400)

    data = []
    for text in response.text_annotations:
        data.append({
            'description': text.description,
            'vertices': [{'x': vertex.x, 'y': vertex.y} for vertex in text.bounding_poly.vertices]
        })

    return data


def text_to_speech(text: str) -> bytes:
    # Instantiates a client
    client = texttospeech.TextToSpeechClient(client_options=clientOptions)

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(language_code="zh-TW", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    # The response's audio_content is binary.
    return response.audio_content
