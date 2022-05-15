from flask import Flask, request, jsonify
from services.form_recognizer import kiosk_form_recognizer
from services.video_indexer import video_indexer_client as video_indexer

from datetime import datetime

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

    video_upload_id = video_indexer.upload_stream_to_video_indexer(video_bytes, video_name=video.filename + str(datetime.now()))
    info = video_indexer.get_video_info(video_upload_id)
    
    # Already a dict
    return info

@app.route('/video-indexing-status', methods=['GET'])
def check_video_indexing_status():
    video_process_id = request.args.get('video_id')

    info = video_indexer.get_video_info(video_process_id)

    # Already a dict
    return info


app.run(debug=True)
