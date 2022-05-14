from flask import Flask, request, jsonify
from services import form_recognizer

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'name': 'alice', 'email': 'alice@gmail.com'})


@app.route('/identity', methods=['GET'])
def recognize_id():
    content_url = request.args.get('url')
    
    return jsonify(form_recognizer.get_identity(content_url))


app.run(debug=True)
