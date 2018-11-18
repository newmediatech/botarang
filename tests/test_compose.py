from unittest import TestCase

from botarang.contrib.navigation import BreadcrumbsRow, NavigationRow
from botarang.ui import Row, View, Bot, Button

RESPONSE = {}
CONTEXT = {}


START_MESSAGE = {
    "ok": True,
    "result": [
        {
            "update_id": 100000000,
            "message": {
                "message_id": 484,
                "from": {
                    "id": 10000000,
                    "is_bot": False,
                    "first_name": "",
                    "last_name": "",
                    "username": "text",
                    "language_code": "ru"
                },
                "chat": {
                    "id": 10000000,
                    "first_name": "",
                    "last_name": "",
                    "username": "test",
                    "type": "private"
                },
                "date": 1540000000,
                "text": "/start",
                "entities":[
                    {
                        "offset": 0,
                        "length": 6,
                        "type": "bot_command"
                    }
                ]
            }
        }
    ]
}

SECOND_LEVEL_MESSAGE = {
    "ok": True,
    "result": [
        {
            "update_id": 100000000,
            "message": {
                "message_id": 484,
                "from": {
                    "id": 10000000,
                    "is_bot": False,
                    "first_name": "",
                    "last_name": "",
                    "username": "text",
                    "language_code": "ru"
                },
                "chat": {
                    "id": 10000000,
                    "first_name": "",
                    "last_name": "",
                    "username": "test",
                    "type": "private"
                },
                "date": 1540000000,
                "text": "/second",
                "entities":[
                    {
                        "offset": 0,
                        "length": 7,
                        "type": "bot_command"
                    }
                ]
            }
        }
    ]
}

THIRD_LEVEL_MESSAGE = {
    "ok": True,
    "result": [
        {
            "update_id": 100000000,
            "message": {
                "message_id": 484,
                "from": {
                    "id": 10000000,
                    "is_bot": False,
                    "first_name": "",
                    "last_name": "",
                    "username": "text",
                    "language_code": "ru"
                },
                "chat": {
                    "id": 10000000,
                    "first_name": "",
                    "last_name": "",
                    "username": "test",
                    "type": "private"
                },
                "date": 1540000000,
                "text": "/third",
                "entities":[
                    {
                        "offset": 0,
                        "length": 6,
                        "type": "bot_command"
                    }
                ]
            }
        }
    ]
}


class AdminPanel(Row):
    def is_visible(self, context: dict) -> bool:
        return context.get("is_admin", False)


class UserPanel(Row):
    buttons = [
        Button("Start", "/start"),
        Button("Second", "/second"),
        Button("Third", "/third"),
    ]
    def is_visible(self, context: dict) -> bool:
        return not context.get("is_admin", False)


class HomeView(View):
    title = "Home view"
    keyboard = [
        NavigationRow(),
        BreadcrumbsRow(),
        AdminPanel(),
        UserPanel(),
    ]


class SecondView(View):
    title = "Second view"
    keyboard = [
        NavigationRow(),
        BreadcrumbsRow(),
        UserPanel(),
    ]

class ThirdView(View):
    title = "Third view"
    keyboard = [
        NavigationRow(),
        BreadcrumbsRow(),
        UserPanel(),
    ]

class BotForTest(Bot):
    def send_response(self, response, *args, **kwargs):
        global RESPONSE

        keys = list(RESPONSE.keys())

        for key in keys:
            del RESPONSE[key]

        RESPONSE.update(response)

    def load_user_context(self, username, **kwargs):
        return CONTEXT.copy()

    def save_user_context(self, username, context):
        global CONTEXT

        keys = list(CONTEXT.keys())

        for key in keys:
            del CONTEXT[key]

        CONTEXT.update(context)


class ViewTestCase(TestCase):
    def test_view(self):
        global RESPONSE

        bot = BotForTest()

        bot.add_route("/start", HomeView())
        bot.add_route("/second", SecondView())
        bot.add_route("/third", ThirdView())

        bot.handle_updates(START_MESSAGE)

        assert RESPONSE == {
            "text": "",
            "keyboard": {
                "inline_keyboard": [
                    [
                        {"text": "Start", "callback_data": "/start"},
                        {"text": "Second", "callback_data": "/second"},
                        {"text": "Third", "callback_data": "/third"}
                    ]
                ],
                "resize_keyboard": True
            }
        }

        bot.handle_updates(SECOND_LEVEL_MESSAGE)

        assert RESPONSE == {
            "text": "",
            "keyboard": {
                "inline_keyboard": [
                    [
                        {"text": "<- Back", "callback_data": "/start"}
                    ],
                    [
                        {"text": "Home view", "callback_data": "/start"}
                    ],
                    [
                        {"text": "Start", "callback_data": "/start"},
                        {"text": "Second", "callback_data": "/second"},
                        {"text": "Third", "callback_data": "/third"}
                    ]
                ],
                "resize_keyboard": True
            }
        }

        bot.handle_updates(THIRD_LEVEL_MESSAGE)

        assert RESPONSE == {
            "text": "",
            "keyboard": {
                "inline_keyboard": [
                    [
                        {"text": "<- Back", "callback_data": "/second"}
                    ],
                    [
                        {"text": "Home view", "callback_data": "/start"},
                        {"text": "Second view", "callback_data": "/second"}
                    ],
                    [
                        {"text": "Start", "callback_data": "/start"},
                        {"text": "Second", "callback_data": "/second"},
                        {"text": "Third", "callback_data": "/third"}
                    ]
                ],
                "resize_keyboard": True
            }
        }

        bot.handle_updates(START_MESSAGE)

        assert RESPONSE == {
            "text": "",
            "keyboard": {
                "inline_keyboard": [
                    [
                        {"text": "Start", "callback_data": "/start"},
                        {"text": "Second", "callback_data": "/second"},
                        {"text": "Third", "callback_data": "/third"}
                    ]
                ],
                "resize_keyboard": True
            }
        }
