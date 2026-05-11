from dataclasses import dataclass

from ..grid import Grid
from ..styling.fields import UIFieldBuilderMixin


@dataclass(frozen=True)
class StatusBadgeConfig:
    label: str
    attr: str
    true_value: str
    false_value: str
    true_style: str = "success"
    false_style: str = "secondary"


@dataclass
class StatusBadgeSection(Grid):
    type: str = "status_badges"

    @property
    def badges(self):
        return self.items

    @property
    def badge_rows(self):
        return self.rows
    

class StatusBadgesSectionMixin(UIFieldBuilderMixin):
    status_badges = ()

    status_badge_section_title = "Estatus del Objeto"
    status_badge_section_description = (
        "Define el estado actual del objeto dentro del sistema y si su "
        "diligenciamiento es obligatorio para el proceso."
    )
    status_badge_section_columns = 3

    def get_status_badges_config(self):
        return self.status_badges

    def get_status_badge_section_title(self):
        return self.status_badge_section_title

    def get_status_badge_section_description(self):
        return self.status_badge_section_description

    def get_status_badge_section_columns(self):
        return self.status_badge_section_columns

    def get_status_badges(self):
        badges = []

        for config in self.get_status_badges_config():
            badge = self.build_status_badge(config)

            if badge:
                badges.append(badge)

        return badges

    def get_status_badge_section(self):
        return StatusBadgeSection(
            title=self.get_status_badge_section_title(),
            description=self.get_status_badge_section_description(),
            items=self.get_status_badges(),
            columns=self.get_status_badge_section_columns(),
        )