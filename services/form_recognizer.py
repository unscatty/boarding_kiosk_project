from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient

from utils.form_recognizer import recognized_form_to_dict
from env import ENV
from .schemas import IDENTITY_SCHEMA, BOARDING_PASS_SCHEMA
class KioskFormRecognizer:
    def __init__(self, endpoint, key, custom_boarding_pass_model_id):
        self.form_recognizer_client = FormRecognizerClient(endpoint, AzureKeyCredential(key))
        self.boarding_pass_model_id = custom_boarding_pass_model_id

    def extract_from_identity(self, identity_url: str, schema=IDENTITY_SCHEMA) -> dict:
        id_content_from_url = self.form_recognizer_client.begin_recognize_identity_documents_from_url(
            identity_url)

        id_content = id_content_from_url.result()

        return [recognized_form_to_dict(result.fields, schema) for result in id_content]

    def extract_from_boarding_pass(self, boarding_pass_url: str, schema=BOARDING_PASS_SCHEMA) -> dict:
        extraction_process = self.form_recognizer_client.begin_recognize_custom_forms_from_url(model_id=self.boarding_pass_model_id, form_url=boarding_pass_url)
        result_content = extraction_process.result()
        
        return [recognized_form_to_dict(result.fields, schema) for result in result_content]


__form_recognizer_config = ENV.azure.form_recognizer

__endpoint = __form_recognizer_config.endpoint
__key = __form_recognizer_config.key
__custom_model_id = __form_recognizer_config.training.model_id

kiosk_form_recognizer = KioskFormRecognizer(__endpoint, __key, __custom_model_id)