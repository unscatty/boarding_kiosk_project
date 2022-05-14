from os import getenv as os_getenv
from dotenv import load_dotenv
from utils.dict import NestedNamespace

load_dotenv()

__env_values = {
    'azure': {
        'form_recognizer': {
            'endpoint': os_getenv('AZURE_FORM_RECOGNIZER_ENDPOINT'),
            'key': os_getenv('AZURE_FORM_RECOGNIZER_KEY')
        }
    }
}

ENV = NestedNamespace(__env_values)
