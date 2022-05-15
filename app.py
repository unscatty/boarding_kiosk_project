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

@app.route('/boarding-pass', methods=['GET'])
def  recognize_boarding_pass():
    boarding_pass_url = request.args.get('url')

    return jsonify(kiosk_form_recognizer.extract_from_boarding_pass(boarding_pass_url))

@app.route('/upload-video', methods=['POST'])
def upload_video():
    video = request.files['video']
    video_bytes = video.stream.read()

    with open(video.filename, 'wb') as video_file:
        video_file.write(video_bytes)
    
    return jsonify({})

app.run(debug=True)
