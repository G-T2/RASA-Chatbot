from typing import Dict, Text, List, Any
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import requests
import os
import re
from datetime import datetime
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

class ActionTimeBasedGreet(Action):
    def name(self) -> Text:
        return "action_time_based_greet"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_time = datetime.now().hour
        if 5 <= current_time < 12:
            greeting = "Good morning! Welcome to Alberta Educational Centre. How can I assist you today?"
        elif 12 <= current_time < 17:
            greeting = "Good afternoon! Welcome to Alberta Educational Centre. How can I assist you today?"
        else:
            greeting = "Good evening! Welcome to Alberta Educational Centre. How can I assist you today?"
        
        dispatcher.utter_message(text=greeting)
        return []

class ActionProvideLink(Action):
    def name(self) -> Text:
        return "action_provide_link"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        
        if intent == "ask_about_student_id":
            message = "You can look up or apply for an Alberta Student ID here: [Alberta Student Registry](https://learnerregistry.ae.alberta.ca/Home/StartLookup)"
        elif intent == "ask_about_admissions":
            message = "You can find detailed information about our admissions process here: [Admissions Page](https://myaec.ca/admissions/)"
        else:
            message = "I'm sorry, I don't have a specific link for that information. How else can I assist you?"
            
        dispatcher.utter_message(text=message)
        return []

class ActionProvideProgramDetails(Action):
    def name(self) -> Text:
        return "action_provide_program_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        programs = {
            "cybersecurity": ("[Cybersecurity Specialist Diploma](https://myaec.ca/programs/cybersecurity-specialist/)", "prepares you for a career in information security."),
            "cloud": ("[Cloud Engineering Diploma](https://myaec.ca/programs/cloud-engineering/)", "focuses on cloud computing technologies and architectures."),
            "medical office": ("[Medical Office Assistant Diploma](https://myaec.ca/programs/medical-office-administration/)", "trains you for administrative roles in healthcare settings."),
            "digital office": ("[Digital Office Certificate](https://myaec.ca/programs/digital-office/)", "equips you with essential digital skills for modern office environments."),
            "pc technician": ("[PC Technician Certificate](https://myaec.ca/programs/pc-technician/)", "covers hardware and software troubleshooting and maintenance."),
            "it professional": ("[IT Professional Certificate](https://myaec.ca/programs/it-professional/)", "provides a broad foundation in information technology."),
            "security analyst": ("[Security Analyst Certificate](https://myaec.ca/programs/security-analyst-certificate/)", "focuses on network security and threat analysis.")
        }
        
        program_message = "These are all the programs we currently offer at Alberta Educational Centre:\n\n"
        for link, details in programs.values():
            program_message += f"• {link} - {details}\n"
        dispatcher.utter_message(text=program_message)
        return []

class ActionProvideLocation(Action):
    def name(self) -> Text:
        return "action_provide_location"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = "Alberta Educational Centre is located in Calgary, Alberta."
        dispatcher.utter_message(text=message)
        return []

class ActionProvideExactAddress(Action):
    def name(self) -> Text:
        return "action_provide_exact_address"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        address = "5980 Centre Street S, Calgary, AB T2H 0C1"
        message = f"Our campus is located at {address}. You can use this address for GPS navigation or mailing purposes."
        dispatcher.utter_message(text=message)
        return []

class ValidateContactForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_contact_form"

    def validate_first_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate first_name value."""
        if len(slot_value.strip()) < 2:
            dispatcher.utter_message(text="I need your first name to properly address you. Please provide a valid first name.")
            return {"first_name": None}
        return {"first_name": slot_value.strip().title()}

    def validate_last_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate last_name value."""
        if len(slot_value.strip()) < 2:
            dispatcher.utter_message(text="Please provide a valid last name so we can properly record your information.")
            return {"last_name": None}
        return {"last_name": slot_value.strip().title()}

    def validate_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate email input."""
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(email_pattern, slot_value):
            return {"email": slot_value.lower()}
        dispatcher.utter_message(text="I need a valid email address to ensure our advisor can reach you. Please provide an email in the format: example@domain.com")
        return {"email": None}

class ActionSubmitToHubSpot(Action):
    def name(self) -> Text:
        return "action_submit_to_hubspot"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        first_name = tracker.get_slot("first_name")
        last_name = tracker.get_slot("last_name")
        email = tracker.get_slot("email")
        
        hubspot_api_key = os.getenv("HUBSPOT_API_KEY")
        if not hubspot_api_key:
            logger.error("Missing HubSpot API key in environment variables")
            dispatcher.utter_message(
                text="I apologize, but I'm having trouble connecting to our system. Please contact us directly at +1 403 441 2059."
            )
            return []

        contact_data = {
            "properties": {
                "firstname": first_name,
                "lastname": last_name,
                "email": email,
                "source": "AEC Rasa Chatbot",
                "submission_time": datetime.now().isoformat(),
                "last_chatbot_interaction": datetime.now().isoformat(),
                "chatbot_contact_reason": "Program Information Request"
            }
        }

        headers = {
            "Authorization": f"Bearer {hubspot_api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                "https://api.hubapi.com/crm/v3/objects/contacts",
                headers=headers,
                json=contact_data,
                timeout=10
            )

            if response.status_code == 201:
                logger.info(f"Successfully created HubSpot contact for {first_name} {last_name}")
                dispatcher.utter_message(
                    text=f"Thank you {first_name}! I've saved your contact information and one of our advisors will reach out to you shortly with more details about our programs."
                )
            else:
                logger.error(f"HubSpot Error: {response.status_code} - {response.text}")
                dispatcher.utter_message(
                    text="I apologize, but I'm having trouble saving your information. Please contact us directly at +1 403 441 2059."
                )

        except Exception as e:
            logger.error(f"Error submitting to HubSpot: {str(e)}")
            dispatcher.utter_message(
                text="I apologize, but I'm having trouble with your request. Please contact us directly at +1 403 441 2059."
            )

        return []