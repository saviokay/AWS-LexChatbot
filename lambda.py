import os
import logging
import json
import boto3
import time
import dateutil.parser

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# -- Helpers For Response Builders --


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return{
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def confirm_intent(session_attributes, intent_name, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attrubutes, slots):
    return {
        'sessionAttributes': session_attrubutes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


# --- Misc Helper Functions ---


def safe_int(n):
    """
    Safely converting n value to integer.
    """
    if n is not None:
        return int(n)
    return n


def isvalid_date(date):
    try:
        dateutil.parser.parse(date)
        return True
    except ValueError:
        return False


def build_validation_result(is_valid, violated_slot, message_content):
    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {
            'contentType': 'PlainText',
            'content': message_content
        }
    }


def isvalid_qtype(qtype):
    qtype = ['liability insurance', 'collision coverage',
             'comprehensive coverage', 'personal injury protection',
             'underinsured motorist protection']
    return qtype.lower() in car_type


def isvalid_add(street, city):
    auth_id = "14324411-3afb-6b5f-8ba0-79b4c7a26694"
    auth_token = "rkJ6XCrMNo5JbuVAkmqp"

    credentials = StaticCredentials(auth_id, auth_token)

    client = ClientBuilder(credentials).build_us_street_api_client()

    lookup = Lookup()
    lookup.street = street
    look.city = city
    lookup.state = "MD"

    try:
        client.send_lookup(lookup)
    except exceptions.SmartyException as err:
        print(err)
        return

    result = lookup.result

    if not result:
        print("No candidates. This means the address is not valid.")
        return False

    first_candidate = result[0]

    print("Address is valid. (There is at least one candidate)\n")
    print("ZIP Code: " + first_candidate.components.zipcode)
    print("County: " + first_candidate.metadata.county_name)
    print("Latitude: {}".format(first_candidate.metadata.latitude))
    print("Longitude: {}".format(first_candidate.metadata.longitude))
    qwe = first_candidate.components.zipcode

    if qwe is not None:
        return True
    else:
        return False


def build_validation_result(isvalid, violated_slot, message_content):
    return {
        'isValid': isvalid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }
