from dataclasses import dataclass

from .icons import UIIconMixin
from .styles import UIStyleMixin


@dataclass
class Button:
    label: str
    url: str
    button_class: str
    icon_class: str | None = None
    type: str = "button"


class UIButtonBuilderMixin(UIStyleMixin, UIIconMixin):
    def build_button(self, label, url, style=None, icon=None):
        return Button(
            label=label,
            url=url,
            button_class=self.get_ui_class(
                component="button",
                style=style or self.DEFAULT_BUTTON_STYLE,
            ),
            icon_class=self.get_icon_class(icon),
        )

    def build_edit_button(self, url):
        return self.build_button(
            label="Editar",
            url=url,
            style="primary",
            icon="edit",
        )

    def build_delete_button(self, url):
        return self.build_button(
            label="Eliminar",
            url=url,
            style="danger",
            icon="delete",
        )