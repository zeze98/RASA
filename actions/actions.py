# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Text, Dict, Any, List

from rasa.shared.core.constants import ACTION_DEFAULT_FALLBACK_NAME
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher


class ActionSetName(Action):
    def name(self):
        return "action_set_name"

    def run(self, dispatcher, tracker, domain):
        name = tracker.get_slot("name")
        dispatcher.utter_message(text=f"name from slots: {name}")
        return []


class ActionCheckName(Action):
    def name(self):
        return "action_check_name"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_action_name["intent"].get("name")

        if intent == "affirm":
            return [SlotSet("CheckName", True)]
        elif intent == "deny":
            return [SlotSet("ChckName", False)]
        return []