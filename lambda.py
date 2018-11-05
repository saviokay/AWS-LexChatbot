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
