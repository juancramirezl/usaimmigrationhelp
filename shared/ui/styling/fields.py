from dataclasses import dataclass

from .styles import UIStyleMixin


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


class UIFieldBuilderMixin(UIStyleMixin):
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
    
    def build_status_badge(self, config):
        if not hasattr(self.object, config.attr):
            return None

        raw_value = getattr(self.object, config.attr)

        if not isinstance(raw_value, bool):
            raise TypeError(
                f"StatusBadgeConfig attr='{config.attr}' must point to a boolean value. "
                f"Got {type(raw_value).__name__} instead."
            )

        return self.build_badge_field(
            label=config.label,
            value=config.true_value if raw_value else config.false_value,
            style=config.true_style if raw_value else config.false_style,
        )
    
    def get_display_field_value(self, attr):
        return getattr(self.object, attr, None)

    def build_display_field(self, config):
        value = self.get_display_field_value(config.attr)

        if value in (None, ""):
            return None

        return self.build_text_field(config.label, value)