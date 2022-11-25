# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import os
from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk.executor import CollectingDispatcher
import requests
import logging

logger = logging.getLogger(__name__)
from rasa_sdk.events import (
    AllSlotsReset,
    SlotSet,
    EventType,
    ActionExecuted,
    SessionStarted,
    Restarted,
    FollowupAction,
)

ACTION_LISTEN_NAME = "action_listen"


def default_actions() -> List['Action']:
    """List default actions."""
    return [ActionListen()]


def default_action_names() -> List[Text]:
    """List default action names."""
    return [a.name() for a in default_actions()]


class ActionListen(Action):
    """The first action in any turn - bot waits for a user message.
    The bot should stop taking further actions and wait for the user to say
    something."""

    def name(self) -> Text:
        return ACTION_LISTEN_NAME

    async def run(self, dispatcher, tracker, domain):
        return []


class ActionNickname(FormAction):
    def name(self) -> Text:
        return "form_action_nickname"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['nickname']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "nickname": self.from_text()
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        nickname = tracker.get_slot('nickname')
        dispatcher.utter_message(
            text="안녕하세요.저는 %s님의 이야기를 들어드릴 챗봇입니다. 오늘 %s님이 하고 싶은 이야기를 편하게 말씀해주시면 됩니다." % (nickname, nickname))

        return [SlotSet("nickname", nickname)]


class ActionStart(FormAction):
    def name(self) -> Text:
        return "form_action_start"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['nickname']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "nickname": self.from_entity("nickname")
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        nickname = tracker.get_slot('nickname')
        dispatcher.utter_message(text="%s님의 이야기를 듣기 전에 몇 가지 이야기 규칙을 말씀드리고 시작하도록 하겠습니다." % (nickname))
        dispatcher.utter_message(
            text="먼저 %s님께서 저에게 %s님에게 있었던 일을 말씀해주실 때, 있었던 일 사실 그대로 말씀해주시면 됩니다." % (nickname, nickname))
        dispatcher.utter_message(text="그리고 제가 %s님에게 질문했을 때 질문에 대한 답을 모르신다면 “모르겠어요”라고 말씀해주세요." % (nickname))
        dispatcher.utter_message(
            text="또 제가 틀리게 이야기한 것이 있으면 바로 고쳐주세요. 마지막으로 %s님에게 있었던 일을 저에게 최대한 자세히 말씀해주시면 됩니다." % (nickname))
        dispatcher.utter_message(text="이해가 되셨다면 '네'를 입력해주세요")
        return []


class ActionRapo1(FormAction):
    def name(self) -> Text:
        return "form_action_rapo1"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['nickname']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "nickname": self.from_entity("nickname")
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        nickname = tracker.get_slot('nickname')
        dispatcher.utter_message(
            text="대화를 시작하기 전에 저는 %s님에 대해서 더 많이 알고 싶고 가까워지고 싶기 때문에 몇 가지 질문을 드릴 거에요 :) " % (nickname))
        dispatcher.utter_message(text="%s님은 무엇을 좋아하시나요? 취미, 음식, 색 등 어떤 것이든 상관없어요." % (nickname))
        return []


class ActionRapo2(FormAction):
    def name(self) -> Text:
        return "form_action_rapo2"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['nickname']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "nickname": self.from_entity("nickname")
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        nickname = tracker.get_slot('nickname')
        dispatcher.utter_message(text="그러시군요! 그럼 방금 말씀하신 %s님이 좋아하시는 것에 대해서 조금 더 말씀해주세요." % (nickname))
        return []


class ActionRapo4(FormAction):
    def name(self) -> Text:
        return "form_action_rapo4"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['nickname']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "nickname": self.from_entity("nickname")
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        nickname = tracker.get_slot('nickname')
        dispatcher.utter_message(
            text="%s님이 좋아하시는 것에 대해서 너무 잘 말씀해주셔서 감사합니다. 덕분에 제가 %s님에 대해서 조금 더 잘 알게 된 것 같아요 :)" % (nickname, nickname))
        return []


class ActionStorystart(FormAction):
    def name(self) -> Text:
        return "form_action_storystart"

    @staticmethod
    def required_slots(tracker) -> List[Text]:
        return ['nickname']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "nickname": self.from_entity("nickname")
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        nickname = tracker.get_slot('nickname')
        dispatcher.utter_message(text="지금부터는 %s님께서 오늘 저에게 해주실 이야기를 처음부터 끝까지 모두 이야기 해주세요." % (nickname))
        return []
