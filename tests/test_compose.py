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

DEMO_MESSAGE = {
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
                "text": "/demo",
                "entities":[
                    {
                        "offset": 0,
                        "length": 5,
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
        Button("Demo", "/demo")
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


class DemoView(View):
    title = "Demo view"
    keyboard = [
        NavigationRow(),
        BreadcrumbsRow()
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
        bot.add_route("/demo", DemoView())

        bot.handle_updates(START_MESSAGE)

        assert RESPONSE == {
            "text": "",
            "keyboard": {
                "inline_keyboard": [
                    [
                        {"text": "Demo", "callback_data": "/demo"}
                    ]
                ],
                "resize_keyboard": True
            }
        }

        bot.handle_updates(DEMO_MESSAGE)

        assert RESPONSE == {
            "text": "",
            "keyboard": {
                "inline_keyboard": [
                    [
                        {"text": "<- Back", "callback_data": "/start"}
                    ],
                    [
                        {"text": "Home view", "callback_data": "/start"}
                    ]
                ],
                "resize_keyboard": True
            }
        }
