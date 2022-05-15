from uuid import uuid4
from time import sleep
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import TrainingStatusType
from msrest.authentication import CognitiveServicesCredentials
from env import ENV

__face_api_config = ENV.azure.face_api

face_client = FaceClient(__face_api_config.endpoint,
                         CognitiveServicesCredentials(__face_api_config.key))

def build_person_group_from_streams(
        stream_images,
        client: FaceClient = face_client,
        person_group_id=str(uuid4()),
        person_group_name='random_person_group' + str(uuid4()),
        person_group_person_name='random_person'+str(uuid4())):
    client.person_group.create(person_group_id, person_group_name)

    face_person = client.person_group_person.create(
        person_group_id, person_group_person_name)

    for stream_image in stream_images:
        client.person_group_person.add_face_from_stream(
            stream_image, face_person.person_id)

    client.person_group.train(person_group_id)

    while (True):
        training_status = client.person_group.get_training_status(
            person_group_id)
        print("Training status: {}.".format(training_status.status))

        if (training_status.status is TrainingStatusType.succeeded):
            return person_group_id
        elif (training_status.status is TrainingStatusType.failed):
            client.person_group.delete(person_group_id=person_group_id)
            raise Exception(
                f'Training the person group with id {person_group_id} has failed.')
        sleep(5)

def detect_faces_ids_from_stream(stream_image, face_client: FaceClient = face_client):
  detected_faces = face_client.face.detect_with_stream(stream_image)
  return [detected_face.face_id for detected_face in detected_faces]

def identity_face_from_person_group(detected_faces_ids, person_group_id, face_client: FaceClient=face_client):
  identification_result = face_client.face.identify(detected_faces_ids, person_group_id)

  for result in identification_result:
    if result.candidates:
        for candidate in result.candidates:
            print("The Identity match confidence is {}".format(candidate.confidence))
    else:
        print("Can't verify the identity with the person group")

  return identification_result