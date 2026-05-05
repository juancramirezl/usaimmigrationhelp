from dataclasses import dataclass


@dataclass
class TextField:
    label: str
    value: object
    type: str = "text"


@dataclass
class BadgeField:
    label: str
    value: object
    badge_class: str
    type: str = "badge"


@dataclass
class Button:
    label: str
    url: str
    button_class: str
    icon_class: str | None = None
    type: str = "button"


class UIBuilderMixin:
    DEFAULT_STYLE = "secondary"
    DEFAULT_BUTTON_STYLE = "primary"

    UI_STYLES = {
        "success": {
            "badge": "bg-success",
            "button": "btn btn-success",
        },
        "danger": {
            "badge": "bg-danger",
            "button": "btn btn-danger",
        },
        "warning": {
            "badge": "bg-warning",
            "button": "btn btn-warning text-dark",
        },
        "info": {
            "badge": "bg-info text-dark",
            "button": "btn btn-info text-dark",
        },
        "primary": {
            "badge": "bg-primary",
            "button": "btn btn-primary",
        },
        "secondary": {
            "badge": "bg-secondary",
            "button": "btn btn-secondary",
        },
        "dark": {
            "badge": "bg-dark",
            "button": "btn btn-dark",
        },
        "outline-primary": {
            "badge": "bg-primary",
            "button": "btn btn-outline-primary",
        },
        "outline-danger": {
            "badge": "bg-danger",
            "button": "btn btn-outline-danger",
        },
        "outline-secondary": {
            "badge": "bg-secondary",
            "button": "btn btn-outline-secondary",
        },
    }

    ICONS = {
        "edit": "bi bi-pencil-fill",
        "delete": "bi bi-trash-fill",
        "add": "bi bi-plus-circle-fill",
        "view": "bi bi-eye-fill",
        "back": "bi bi-arrow-left",
    }

    def get_ui_class(self, component, style=None):
        style = style or self.DEFAULT_STYLE

        style_config = self.UI_STYLES.get(
            style,
            self.UI_STYLES[self.DEFAULT_STYLE],
        )

        return style_config.get(component, "")
    
    def get_icon_class(self, icon=None):
        if not icon:
            return None

        return self.ICONS.get(icon)

    def build_text_field(self, label, value):
        return TextField(
            label=label,
            value=value,
        )

    def build_badge_field(self, label, value, style=None):
        return BadgeField(
            label=label,
            value=value,
            badge_class=self.get_ui_class("badge", style),
        )
    
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
            icon="edit"
        )

    def build_delete_button(self, url):
        return self.build_button(
            label="Eliminar",
            url=url,
            style="danger",
            icon="delete"
        )