import os
import traceback
import logging
from dynacloud import service, exceptions
from werkzeug.exceptions import HTTPException
from google.api_core.exceptions import GoogleAPICallError
from flask import Flask, jsonify, json, request, make_response, abort


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webep'}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000


@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()

    # replace the body with JSON
    response.content_type = "application/json"
    response.data = json.dumps({"errors": [e.description]})

    return response


@app.errorhandler(GoogleAPICallError)
def handle_google_api_error(e):
    logging.warning(e.message)
    return make_response(jsonify({"errors": [e.message]}), e.code)


@app.errorhandler(exceptions.CustomException)
def handle_custom_exception(e):
    logging.warning(e.message)
    return make_response(jsonify({"errors": [e.message]}), e.code)


@app.errorhandler(Exception)
def handle_exceptions(e):
    filename, line_num, func_name, text = traceback.extract_tb(e.__traceback__)[-1]
    logging.info(e)
    logging.info(f'Exception;main;{type(e).__name__};MSG;{str(e)};FILE;{filename};LINE;{line_num};FUNC;{func_name};TEXT;{text}')

    return make_response(jsonify({"errors": ['Internal Server Error']}), 500)


@app.before_request
def before_request():
    auth_header = request.headers.get('Authorization')
    token = service.parse_token_from_auth_header(auth_header)
    service.check_auth_token_is_valid(token)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    return jsonify({'data': 'Hello AIoT!'})


@app.route('/vision', methods=['POST'])
def vision():
    file = request.files.get('image')

    if not file:
        abort(422, 'Please upload the image using the image parameter.')
    if not allowed_file(file.filename) or file.filename == '':
        abort(422, 'Unsupported image type.')
    else:
        data = service.detect_text(file)
        return jsonify({'data': data})


if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=True, port=server_port, host='0.0.0.0')
