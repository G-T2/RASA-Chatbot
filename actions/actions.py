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
        
        dispatcher.utter_message(text=f"{greeting} Welcome to Alberta Education Consultants. How can I assist you today?")
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
        elif intent == "ask_about_programs":
            link = "https://myaec.ca/programs/"
            message = f"You can view all our programs here: {link}. Is there a specific field you're interested in?"
        else:
            message = "I'm sorry, I don't have a specific link for that information. How else can I assist you?"
        dispatcher.utter_message(text=message)
        return []

class ActionProvideProgramDetails(Action):
    def name(self) -> Text:
        return "action_provide_program_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        programs = {
            "cybersecurity": "Our Cybersecurity Specialist Diploma program prepares you for a career in information security.",
            "cloud": "The Cloud Engineering Diploma program focuses on cloud computing technologies and architectures.",
            "medical office": "The Medical Office Assistant Diploma program trains you for administrative roles in healthcare settings.",
            "digital office": "Our Digital Office Certificate program equips you with essential digital skills for modern office environments.",
            "pc technician": "The PC Technician Certificate program covers hardware and software troubleshooting and maintenance.",
            "it professional": "The IT Professional Certificate program provides a broad foundation in information technology.",
            "security analyst": "Our Security Analyst Certificate program focuses on network security and threat analysis."
        }
        
        user_message = tracker.latest_message['text'].lower()
        for keyword, details in programs.items():
            if keyword in user_message:
                dispatcher.utter_message(text=details)
                return []
        
        dispatcher.utter_message(text="I'm not sure which specific program you're asking about. We offer diploma programs in Cybersecurity, Cloud Engineering, and Medical Office Assistance, as well as certificate programs in Digital Office, PC Technician, IT Professional, and Security Analyst fields. You can find more details about all our programs at https://myaec.ca/programs/")
        return []

class ActionProvideLocation(Action):
    def name(self) -> Text:
        return "action_provide_location"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        if intent == "ask_location":
            message = "Alberta Education Consultants is located in Calgary, Alberta."
        elif intent == "ask_exact_address":
            message = "Our campus is located at 5980 Centre Street S, Calgary, AB T2H 0C1."
        else:
            message = "I'm sorry, I couldn't determine what location information you need. Can you please clarify?"
        dispatcher.utter_message(text=message)
        return []