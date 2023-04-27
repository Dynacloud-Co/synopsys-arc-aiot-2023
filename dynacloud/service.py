import logging
from flask import abort
from werkzeug.datastructures import FileStorage
from .config import GOOGLE_API_KEY, APP_AUTH_TOKEN
from .exceptions import *
from google.cloud import vision
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
