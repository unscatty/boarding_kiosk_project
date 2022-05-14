from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient

from utils.dict import partial_dict
from env import ENV

form_recognizer_config = ENV.azure.form_recognizer

endpoint = form_recognizer_config.endpoint
key = form_recognizer_config.key

form_recognizer_client = FormRecognizerClient(
    endpoint=endpoint, credential=AzureKeyCredential(key))


def get_identity(content_url: str, fields=['Address', 'FirstName', 'LastName', 'Sex', 'DateOfBirth'], properties=['value', 'confidence']) -> dict:
    id_content_from_url = form_recognizer_client.begin_recognize_identity_documents_from_url(
        content_url)

    id_content = id_content_from_url.result()

    schema = {field: properties for field in fields}

    return [partial_dict(result.fields, key=schema) for result in id_content]
