from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient

from utils.dict import partial_dict
from env import ENV
class KioskFormRecognizer:
    def __init__(self, endpoint, key):
        self.form_recognizer_client = FormRecognizerClient(
            endpoint=endpoint, credential=AzureKeyCredential(key))

    def extract_from_identity(self, content_url: str, fields=['Address', 'FirstName', 'LastName', 'Sex', 'DateOfBirth'], properties=['value', 'confidence']) -> dict:
        id_content_from_url = self.form_recognizer_client.begin_recognize_identity_documents_from_url(
            content_url)

        id_content = id_content_from_url.result()

        schema = {field: properties for field in fields}

        return [partial_dict(result.fields, key=schema) for result in id_content]


__form_recognizer_config = ENV.azure.form_recognizer

__endpoint = __form_recognizer_config.endpoint
__key = __form_recognizer_config.key

kiosk_form_recognizer = KioskFormRecognizer(__endpoint, __key)