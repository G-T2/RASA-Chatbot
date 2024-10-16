from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime

class ActionTimeBasedGreet(Action):
    def name(self) -> Text:
        return "action_time_based_greet"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        current_time = datetime.now().hour
        if 5 <= current_time < 12:
            greeting = "Good morning!"
        elif 12 <= current_time < 17:
            greeting = "Good afternoon!"
        else:
            greeting = "Good evening!"
        
        dispatcher.utter_message(text=f"{greeting} Welcome to Alberta Educational Centre. How can I assist you today?")
        return []

class ActionProvideLink(Action):
    def name(self) -> Text:
        return "action_provide_link"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if intent == "ask_about_student_id":
            link = "https://learnerregistry.ae.alberta.ca/Home/StartLookup"
            message = f"You can look up or apply for an Alberta Student ID here: {link}"
        elif intent == "ask_about_admissions":
            link = "https://myaec.ca/admissions/"
            message = f"You can find detailed information about our admissions process here: {link}"
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
        
        user_message = tracker.latest_message['text'].lower()
        for keyword, (link, details) in programs.items():
            if keyword in user_message:
                message = f"Our {link} program {details}\n\nHere's a quick list of all our programs:\n\n"
                for l, d in programs.values():
                    message += f"• {l}\n"
                message += "\nWould you like more information about any other program?"
                dispatcher.utter_message(text=message)
                return []
        
        message = "I'm not sure which specific program you're asking about. We offer the following programs:\n\n"
        for link, details in programs.values():
            message += f"• {link}\n"
        message += "\nYou can find more details about all our programs at https://myaec.ca/programs/. Which program interests you most?"
        dispatcher.utter_message(text=message)
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