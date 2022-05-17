from flask import Flask, request, jsonify
from services.form_recognizer import kiosk_form_recognizer
from services import video_indexer as video_indexer_service
from services.video_indexer import video_indexer_client
from services import face as face_service
from services import custom_vision as custom_vision_service
from services import validation as validation_service
from services.flight_manifest import flight_manifest as flight_manifest_service

from utils.dict import partial_dict, to_dict

from datetime import datetime

app = Flask(__name__)

global flight_manifest_row
flight_manifest_row = {}


@app.route('/identity', methods=['GET'])
def recognize_id():
    content_url = request.args.get('url')

    return jsonify(kiosk_form_recognizer.extract_from_identity(content_url))


@app.route('/identity-file', methods=['POST'])
def recognize_id_file():
    id_document_file = request.files['id_document'].stream

    is_valid, response, row = validation_service.validate_identity_document(
        id_document_file, flight_manifest_row, flight_manifest_service)

    if is_valid:
        return response, 200
    else:
        return {'error': response}, 478

    # return jsonify(kiosk_form_recognizer.extract_from_identity_file(id_document_file))


@app.route('/boarding-pass', methods=['GET'])
def recognize_boarding_pass():
    boarding_pass_url = request.args.get('url')

    return jsonify(kiosk_form_recognizer.extract_from_boarding_pass(boarding_pass_url))


@app.route('/boarding-pass-file', methods=['POST'])
def recognize_boarding_pass_from_file():
    boarding_pass_file = request.files['boarding_pass'].stream

    is_valid, response, row = validation_service.validate_boarding_pass(
        boarding_pass_file, flight_manifest_service)

    global flight_manifest_row
    flight_manifest_row = row

    if is_valid:
        return response, 200
    else:
        return {'error': response}, 478

    # return jsonify(kiosk_form_recognizer.extract_from_boarding_pass_file(boarding_pass_file))


@app.route('/upload-video', methods=['POST'])
def upload_video():
    video = request.files['video']
    video_bytes = video.stream.read()

    video_upload_id = video_indexer_client.upload_stream_to_video_indexer(
        video_bytes, video_name=video.filename + str(datetime.now()))
    info = video_indexer_client.get_video_info(video_upload_id)

    # Already a dict
    return info


@app.route('/video-indexing-status', methods=['GET'])
def check_video_indexing_status():
    video_process_id = request.args.get('video_id')

    info = video_indexer_client.get_video_info(video_process_id)

    # Already a dict
    return info


@app.route('/video-analysis', methods=['GET'])
def video_analysis():
    video_id = request.args.get('video_id')

    analysis = video_indexer_service.get_video_analysis(video_id)

    return analysis


@app.route('/detect-identity', methods=['POST'])
def detected_from_id_document():
    video_id = request.args.get('video_id')
    id_document_stream = request.files['id_document'].stream

    is_valid, response, row = validation_service.validate_identity_from_video(id_document_stream, video_id, None)

    if is_valid:
        return response, 200
    else:
        return {'error': response}, 478

@app.route('/validate-baggage', methods=['POST'])
def validate_baggage():
    baggage_image = request.files['baggage'].stream

    prediction_results = custom_vision_service.detect_with_stream(
        baggage_image)

    return jsonify(partial_dict(to_dict(prediction_results), ['probability', 'tag_type']))


if __name__ == '__main__':
    app.run()
