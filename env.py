from os import getenv as os_getenv
from dotenv import load_dotenv
from utils.dict import NestedNamespace

load_dotenv()

__env_values = {
    'azure': {
        'form_recognizer': {
            'endpoint': os_getenv('AZURE_FORM_RECOGNIZER_ENDPOINT'),
            'key': os_getenv('AZURE_FORM_RECOGNIZER_KEY'),
            'training': {
                'model_id': os_getenv('AZURE_FORM_RECOGNIZER_CUSTOM_MODEL_ID'),
                'model_name': os_getenv('AZURE_FORM_RECOGNIZER_CUSTOM_MODEL_NAME'),
                'training_data': {
                    'url': os_getenv('AZURE_FORM_RECOGNIZER_CUSTOM_MODEL_TRAIN_DATA_URL'),
                    'subfolder': os_getenv('AZURE_FORM_RECOGNIZER_CUSTOM_MODEL_TRAIN_DATA_SUBFOLDER')
                }
            }
        },
        'video_indexer': {
            'subscription_key': os_getenv('AZURE_VIDEO_INDEXER_SUBSCRIPTION_KEY'),
            'location': os_getenv('AZURE_VIDEO_INDEXER_LOCATION'),
            'account_id': os_getenv('AZURE_VIDEO_INDEXER_ACCOUNT_ID')
        },
        'face_api': {
            'endpoint': os_getenv('AZURE_FACE_API_ENDPOINT'),
            'key': os_getenv('AZURE_FACE_API_KEY')
        },
        'custom_vision': {
            'training': {
                'endpoint': os_getenv('AZURE_CUSTOM_VISION_TRAINING_ENDPOINT'),
                'key': os_getenv('AZURE_CUSTOM_VISION_TRAINING_KEY'),
            },
            'prediction': {
                'endpoint': os_getenv('AZURE_CUSTOM_VISION_PREDICTION_ENDPOINT'),
                'key': os_getenv('AZURE_CUSTOM_VISION_PREDICTION_KEY'),
                'resource_id': os_getenv('AZURE_CUSTOM_VISION_PREDICTION_RESOURCE_ID')
            },
            'custom_project': {
                'name': os_getenv('AZURE_CUSTOM_VISION_PROJECT_NAME'),
                'project_id': os_getenv('AZURE_CUSTOM_VISION_PROJECT_ID'),
                'iteration_id': os_getenv('AZURE_CUSTOM_VISION_PROJECT_ITERATION_ID'),
                'iteration_name': os_getenv('AZURE_CUSTOM_VISION_PROJECT_ITERATION_NAME'),
                # Get every tag separated by a comma
                'tags': [tag.strip() for tag in os_getenv('AZURE_CUSTOM_VISION_PROJECT_TAGS').split(',')]
            }
        }
    }
}

ENV = NestedNamespace(__env_values)
