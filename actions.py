# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.interfaces import Action
from rasa_sdk.events import SlotSet, AllSlotsReset

import smtplib
import imghdr
from email.message import EmailMessage
import re,os
from dotenv import load_dotenv

load_dotenv()
EMAIL_PATTERN = "^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$"
NAME_PATTERN = "^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$"


class ValidateContactForm(FormValidationAction):

    
    def name(self) -> Text:
        return "validate_contact_form"

    def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate name value."""

        value = str(slot_value)

        if len(value) < 2:  # Minumum name length
            dispatcher.utter_message(response="utter_invalid_name")
            return {"name" : None}

        pattern = re.compile(NAME_PATTERN)
        valid_name = pattern.match(str(value).strip())
        if not valid_name:
            dispatcher.utter_message(response="utter_invalid_name")
            return {"name" : None}
        
        return {"name" : value}

    def validate_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate email value."""

        value = str(slot_value)

        pattern = re.compile(EMAIL_PATTERN)
        valid_email = pattern.match(str(value).strip())
        if not valid_email:
            dispatcher.utter_message(response="utter_invalid_email")
            return {"email":None}

        return {"email": value}

    def validate_message(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate messgae value."""

        value = str(slot_value)

        if len(value) < 5:
            dispatcher.utter_message(response="utter_invalid_msg")
            return {"message": None}
        return {"message": value}

class ActionSubmitContactForm(Action):

    def name(self):
        return 'action_submit_contact_form'

    @staticmethod
    def send_email(user_name, user_email, user_msg):
        
        EMAIL_PASSWORD = os.getenv('EMAIL_PASS')
        EMAIL_ADDRESS = 'pratamesh1867@gmail.com'

        # print(EMAIL_ADDRESS, EMAIL_PASSWORD, user_name, user_email, user_msg)
        msg = EmailMessage()
        msg['Subject'] = 'PORTFOLIO | Message from: '+str(user_name)
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg['Bcc'] = user_email
        msg.set_content("Name: "+user_name+"\nEmail: "+user_email+"\nMessage: "+user_msg+"\n\n You have received this copy as you messaged from Know-Me-Bot.")
        msg.add_alternative("""\
            <!DOCTYPE html>
            <html>
                <body>
                    <p><b>Name: </b>"""+user_name+"""</p>
                    <p><b>Email: </b>"""+user_email+"""</p>
                    <p><b>Message: </b>"""+user_msg+"""</p>
                    <p>
                        <i>You have received this copy as you messaged from Know-Me-Bot.</i>
                    </p>
                </body>
            </html>
            """, subtype='html')
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            smtp.quit()

    async def run(self, dispatcher, tracker, domain):
        name = tracker.get_slot('name')
        email = tracker.get_slot('email')
        msg = tracker.get_slot('message')

        # dispatcher.utter_message(response='utter_wait_for_email')
        ActionSubmitContactForm.send_email(name, email, msg)

        dispatcher.utter_message(response='utter_contact_form_submit',name=name)
        return [SlotSet("message", None)]

class ActionBye(Action):

    def name(self):
        return 'action_bye'

    async def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response='utter_bye')
        return [AllSlotsReset()]

class ActionContactFormSuccess(Action):

    def name(self):
        return 'action_contact_success'

    async def run(self, dispatcher, tracker, domain):
        name = tracker.get_slot('name')
        dispatcher.utter_message(response='utter_contact_form_success',name=name)
        return []