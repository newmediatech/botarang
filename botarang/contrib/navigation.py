from botarang.errors import BotConfigException
from botarang.ui import Button, Row


class BackButton(Button):
    title = "<- Back"

    def is_visible(self, context: dict) -> bool:
        breadcrumbs = context.get("breadcrumbs", ["/start"])
        return len(breadcrumbs) > 1

    def get_callback_data(self, context) -> str:
        breadcrumbs = context.get("breadcrumbs", ["/start"])
        return breadcrumbs[-2]


class NavigationRow(Row):
    buttons = [
        BackButton()
    ]


class BreadcrumbsRow(Row):
    def get_buttons(self, context):
        breadcrumbs = context.get("breadcrumbs", ["/start"])

        buttons = []

        for raw_url in breadcrumbs[:-1]:
            if ":" in raw_url:
                url, parameter = raw_url.split(":")
            else:
                url = raw_url
                parameter = ""

            view = context["bot"].routes.get(url)

            if not view:
                raise BotConfigException("View does not exist")

            buttons.append(
                Button(title=view.get_title(context), path=url, parameter=parameter)
            )

        return buttons


class PaginatorRow(Row):
    def get_buttons(self, context):
        raise NotImplementedError


class ScrollTopRow(Row):
    def get_buttons(self, context):
        raise NotImplementedError


class ScrollBottomRow(Row):
    def get_buttons(self, context):
        raise NotImplementedError


class SlideRow(Row):
    def get_buttons(self, context):
        raise NotImplementedError
