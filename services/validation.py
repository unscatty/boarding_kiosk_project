from services.form_recognizer import kiosk_form_recognizer as form_recognizer_service
from services.flight_manifest import FlightManifest
from datetime import datetime

from env import ENV

__fligh_manifest_config = ENV.flight_manifest

# Format: {'Flight manifest column': 'Extracted Boarding Pass Field' }
boarding_pass_validation_schema = {
    'PassengerName': 'passengerName',
    'Carrier': 'carrier',
    'FlightNo': 'flightNumber',
    'Class': 'class',
    'From': 'from',
    'To': 'to',
    # Date extracted from boarding pass is wrong, use alternate field value instead
    'Date': 'dateAlt',
    'Baggage': 'baggage',
    'Seat': 'seat',
    'Gate': 'gate',
    'BoardingTime': 'boardingTime',
    'BoardingPassID': 'boardingPassId',
}

def validate_boarding_pass(boarding_pass_file, flight_manifest: FlightManifest, validation_schema=boarding_pass_validation_schema, find_by_property='BoardingPassID', validation_column='BoardingPassValidation'):
    extracted_data = form_recognizer_service.extract_from_boarding_pass_file(
        boarding_pass_file)

    if len(extracted_data) != 1:
        # More than one documents
        return False, 'Service detected more than one boarding pass documents'

    boarding_pass_data = extracted_data[0]

    # Get corresponding row from fligt manifest
    try:
        flight_manifest_row = flight_manifest.find(key=find_by_property, value=boarding_pass_data.get(validation_schema[find_by_property]).get('value'))
    except StopIteration:
        return False, 'Could not find your boarding pass information in flight manifest'

    # Validate each field with its corresponding column in flight manifest
    for flight_manifest_key, boarding_pass_key in validation_schema.items():
        # Compare values from extracted data with values from flight manifest
        # In extracted data actual text value is in "value" key
        boarding_pass_value = boarding_pass_data[boarding_pass_key]['value']
        flight_manifest_value = flight_manifest_row[flight_manifest_key]

        # Tranform 'Economy' to 'E', and 'Business' to 'B'
        if flight_manifest_key == 'Class':
          flight_manifest_value = flight_manifest_value[0].upper()

        if flight_manifest_value.strip() != boarding_pass_value.strip():
            return False, (f'Field "{flight_manifest_key}" with value "{flight_manifest_value}"'
                           ' from flight manifest did not match '
                           f'"{boarding_pass_key}" with value "{boarding_pass_value}" from boarding pass')

    # Change flight manifest
    flight_manifest_row[validation_column] = str(True).upper()

    # Update flight manifest
    flight_manifest.upload()

    return True, boarding_pass_data

def validate_identity_document(identity_doc_file, flight_manifest: FlightManifest, date_format = __fligh_manifest_config.date_format):
    extracted_data = form_recognizer_service.extract_from_identity_file(identity_doc_file)

    if len(extracted_data) != 1:
        # More than one documents
        return False, 'Service detected more than one identity documents'

    id_document_data = extracted_data[0]

    # Full name from identity document
    id_document_name = id_document_data['firstname']['value'] + ' ' + id_document_data['lastname']['value']
    id_date_of_birth = id_document_data['dateofbirth']['value']

    # Iterate through every row in flight manifest
    for row in flight_manifest.as_list():
        name_validation = row['PassengerName'] == id_document_name

        # Transform to datetime.date for comparison
        fligh_manifest_date_of_birth = datetime.strptime(row['DateOfBirth'], date_format).date()

        date_of_birth_validation = id_date_of_birth == fligh_manifest_date_of_birth

        if name_validation and date_of_birth_validation:
            # Valid id document
            row['DoBValidation'] = str(True).upper()
            row['NameValidation'] = str(True).upper()

            # Update flight manifest with validation info
            flight_manifest.upload()

            return True, id_document_data
    
    # Couldn't get info from flight manifest
    return False, 'Your identification data could not be found in flight manifest'

# def 