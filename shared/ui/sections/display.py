from dataclasses import dataclass

from ..grid import Grid
from ..styling.fields import UIFieldBuilderMixin


@dataclass(frozen=True)
class DisplayFieldConfig:
    label: str
    attr: str


@dataclass
class DisplaySection(Grid):
    type: str = "display"

    @property
    def fields(self):
        return self.items

    @property
    def field_rows(self):
        return self.rows
    

class DisplayFieldsSectionMixin(UIFieldBuilderMixin):
    display_fields = ()

    display_section_title = "Información General"
    display_section_description = (
        "Contiene los datos básicos de identificación y configuración del objeto, "
        "necesarios para su organización y referencia dentro del sistema."
    )
    display_section_columns = 3


    def get_display_fields_config(self):
        return self.display_fields
    
    def get_display_section_title(self):
        return self.display_section_title

    def get_display_section_description(self):
        return self.display_section_description

    def get_display_section_columns(self):
        return self.display_section_columns

    def get_display_fields(self):
        fields = []

        for config in self.get_display_fields_config():
            field = self.build_display_field(config)

            if field:
                fields.append(field)

        return fields
    
    def get_display_section(self):
        return DisplaySection(
            title=self.get_display_section_title(),
            description=self.get_display_section_description(),
            items=self.get_display_fields(),
            columns=self.get_display_section_columns(),
        )
