from flask import Flask, request, jsonify
from services.form_recognizer import kiosk_form_recognizer

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'name': 'alice', 'email': 'alice@gmail.com'})


@app.route('/identity', methods=['GET'])
def recognize_id():
    content_url = request.args.get('url')
    
    return jsonify(kiosk_form_recognizer.extract_from_identity(content_url))


app.run(debug=True)
