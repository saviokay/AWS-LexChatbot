import os
import logging
import json
import boto3
import time
import dateutil.parser

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# -- Helpers For Response Builders --

# -- ElicitSlot — Informs Amazon Lex that the user is expected to provide a slot value in the response.


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

# -- ConfirmIntent — Informs Amazon Lex that the user is expected to give a yes or no answer to confirm or deny the current intent.


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

# -- Close — Informs Amazon Lex not to expect a response from the user. For example, "Your pizza order has been placed" does not require a response.


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

# -- Delegate — Directs Amazon Lex to choose the next course of action based on the bot configuration.


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
    """
    Safely checking parsed date to be True.
    """
    try:
        dateutil.parser.parse(date)
        return True
    except ValueError:
        return False


def build_validation_result(is_valid, violated_slot, message_content):
    """
    Making result for Validation
    """
    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {
            'contentType': 'PlainText',
            'content': message_content
        }
    }


def isvalid_qtype(qtype):
    """
    Validation for user created Slot 'Quote Type' - qtype.
    """
    qtype = ['liability insurance', 'collision coverage',
             'comprehensive coverage', 'personal injury protection',
             'underinsured motorist protection']
    return qtype.lower() in car_type


def isvalid_add(street, city):
    """
    Validation for user inputed address and street information.
    """
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


def validate_values(qtype, caddress, cname, clast, city):
    if qtype and not isvalid_qtype(qtype):
        return build_validation_result(False, 'QType', 'I did not recognize that, can you please provide me with a valid insurance type?')

        if caddress and city:
            if isvalid_add('caddress', 'city') is False:
                return build_validation_result(False, 'CAddress', 'This is an invalid Address, Kindly input correct Address')

        return build_validation_result(True, None, None)


def validate_quote(slots):
    caddres = intent_request['currentIntent']['slots']['CAddress']
    cname = intent_request['currentIntent']['slots']['CName']
    clast = intent_request['currentIntent']['slots']['​CLast']
    qtype = intent_request['currentIntent']['slots']['​QType']
    city = intent_request['currentIntent']['slots']['City']
    source = intent_request['invocationSource']
    output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {
    }

    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        slots = intent_request['currentIntent']['slots']
        validation_result = validate_values(qtype, caddress, cname, clast, city)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(
                output_session_attributes,
                intent_request['currentIntent']['name'],
                slots,
                validation_result['violatedSlot'],
                validation_result['message'],
                build_response_card(
                    'Specify {}'.format(validation_result['violatedSlot']),
                    validation_result['message']['content'],
                    build_options(validation_result['violatedSlot'],
                                  appointment_type, date, booking_map)
                )
            )

        if not caddress:
            return elicit_slot(
                output_session_attributes,
                intent_request['currentIntent']['name'],
                intent_request['currentIntent']['slots'],
                'CAddress',
                {'contentType': 'PlainText',
                    'content': 'Please specify a proper address for quotation evaluation'},
                build_response_card(
                    'Specify Address', 'Please specify a proper address for quotation evaluation',
                    build_options('CAddress', caddress, date, None)
                )
            )

    if qtype and not isvalid_quote_type(qtype):
        return build_validation_result(
            False,
            '​QType',
            'We currently do not support {} as a valid insurance type.  Can you try a different type?'.format(qtype))


def get_quote(intent_request):
    caddres = try_ex(lambda: slots['​CAddress'])
    cname = try_ex(lambda: slots['CName'])
    clast = try_ex(lambda: slots['​CLast'])
    qtype = try_ex(lambda: slots['​QType'])
    city = try_ex(lambda: slots['City'])
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {
    }

    # Load confirmation history and track the current reservation.
    reservation = json.dumps({
        'QType': qtype,
        '​CAddress': caddres,
        'CName': cname,
        '​CLast': clast,
        'City': city
    })

    session_attributes['currentReservation'] = reservation
    # Validate any slots which have been specified.  If any are invalid, re-elicit for their value
    if intent_request['invocationSource'] == 'DialogCodeHook':
        validation_result = validate_quote(intent_request['currentIntent']['slots'])
        if not validation_result['isValid']:
            slots = intent_request['currentIntent']['slots']
            slots[validation_result['violatedSlot']] = None

            return elicit_slot(
                session_attributes,
                intent_request['currentIntent']['name'],
                slots,
                validation_result['violatedSlot'],
                validation_result['message']
            )


def greetings(intent_request):
    cname = try_ex(lambda: intent_request['currentIntent']['slots']['CName'].title())
    intent = intent_request['currentIntent']['name']
    slots = intent_request['currentIntent']['slots']
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {
    }

    reservation = json.dumps({
        'CName': cname,
    })

    session_attributes['currentReservation'] = reservation

    logger.info("Hey Thisis is a test")
    logger.info("Intent Name : ")
    logger.info(intent)
    logger.info("Name :  ")
    logger.info(cname)
    logger.info("Slots is :")
    logger.info(slots)

    return delegate(session_attributes, intent_request['currentIntent']['slots'])


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(
        intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'Greetings':
        return greetings(intent_request)
    elif intent_name == 'Info':
        return get_quote(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')

    def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
