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


class StyleBuilderMixin:
    DEFAULT_BADGE_STYLE = "secondary"

    BADGE_STYLES = {
        "success": "bg-success",
        "danger": "bg-danger",
        "warning": "bg-warning",
        "info": "bg-info",
        "primary": "bg-primary",
        "secondary": "bg-secondary",
        "dark": "bg-dark",
    }

    def get_badge_class(self, style=None):
        style = style or self.DEFAULT_BADGE_STYLE

        return self.BADGE_STYLES.get(
            style,
            self.BADGE_STYLES[self.DEFAULT_BADGE_STYLE],
        )

    def build_text_field(self, label, value):
        return TextField(
            label=label,
            value=value,
        )

    def build_badge_field(self, label, value, style=None):
        return BadgeField(
            label=label,
            value=value,
            badge_class=self.get_badge_class(style),
        )