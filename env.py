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
                    'url':os_getenv('AZURE_FORM_RECOGNIZER_CUSTOM_MODEL_TRAIN_DATA_URL'),
                    'subfolder': os_getenv('AZURE_FORM_RECOGNIZER_CUSTOM_MODEL_TRAIN_DATA_SUBFOLDER')
                }
            }
        },
        'video_indexer': {
            'subscription_key': os_getenv('AZURE_VIDEO_INDEXER_SUBSCRIPTION_KEY'),
            'location': os_getenv('AZURE_VIDEO_INDEXER_LOCATION'),
            'account_id': os_getenv('AZURE_VIDEO_INDEXER_ACCOUNT_ID')
        }
    }
}

ENV = NestedNamespace(__env_values)
