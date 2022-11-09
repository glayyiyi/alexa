# -*- coding: utf-8 -*-

# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Amazon Software License (the "License"). You may not use this file except in
# compliance with the License. A copy of the License is located at
#
#    http://aws.amazon.com/asl/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from urllib.request import Request
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name, get_account_linking_access_token, get_request_type, get_intent_name, get_slot_value_v2, get_simple_slot_values 
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard, output_speech
from ask_sdk_model import Response
from ask_sdk_core.skill_builder import SkillBuilder

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
sb = SkillBuilder()



class CheckAccountLinkedHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return not get_account_linking_access_token(handler_input)
        
        
    def handle(self, handler_input):
        print("Can CheckAccountLinkedHandler-------------------------------------------------------")
        return handler_input.response_builder.speak("Need to link account in Alexa App").response



class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        print("Can CancelOrStopIntentHandler-------------------------------------------------------")
        # type: (HandlerInput) -> Response
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """
    This handler will not be triggered except in supported locales,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        print("Can FallbackIntentHandler-------------------------------------------------------")
        # type: (HandlerInput) -> Response
        speech_text = (
            "The Hello World skill can't help you with that.  "
            "You can say hello!!")
        reprompt = "You can say hello!!"
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        print("Can SessionEndedRequestHandler-------------------------------------------------------")
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        print("Can CatchAllExceptionHandler-------------------------------------------------------")
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response
        
        
class SayHelloHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return get_request_type(handler_input) == "IntentRequest" and get_intent_name(handler_input) == 'SayHelloIntent'
    def handle(self, handler_input):
        print("Can SayHelloHandler-------------------------------------------------------")
        logger.info(handler_input.request_envelope)
        logger.info(handler_input.context)
        reprompt_message = "what is your request?"
        #speak_message = "hello " + get_user_name(handler_input)
        speak_message = "hello BYD"
        return handler_input.response_builder.speak(speak_message).ask(reprompt_message).response


class RequestInfoHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        print("handler input request_envelope and context is: ")
        logger.info(handler_input.request_envelope)
        logger.info(handler_input.context)
        
        return is_request_type("IntentRequest")(handler_input) and is_intent_name("RequestInfoIntent")(handler_input)

    def handle(self, handler_input):
        print("Can RequestInfoHandler-------------------------------------------------------")

        output_string = "Status: " + get_status(handler_input) + " Full Status: " + get_full_status(handler_input)
        return handler_input.response_builder.speak("Here is your info, " + output_string).set_card(
            SimpleCard("Hello my BYD", output_string)
        ).response

#custom skill handler function
def get_status(handler_input):
    return "status car door status"

def get_full_status(handler_input):
    return "status full"


sb.add_request_handler(CheckAccountLinkedHandler())
sb.add_request_handler(SayHelloHandler())
sb.add_request_handler(RequestInfoHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler=sb.lambda_handler()
