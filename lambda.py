import os
import logging
import json
import boto3

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
