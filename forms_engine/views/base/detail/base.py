from django.views.generic import DetailView

from .mixins import (
    DefaultTableSectionMixin,
    DefaultAccordionSectionMixin,
    DefaultListSectionMixin,
)


class BaseGenericDetailView(
    DefaultTableSectionMixin,
    DefaultAccordionSectionMixin,
    DefaultListSectionMixin,
    DetailView,
):
    template_name = "forms_engine/generic/detail.html"
    section_meta = "Meta Descripción"

    display_field_map = (
        ("Orden", "order"),
        ("Clave", "key"),
    )

    def get_back_url(self):
        raise NotImplementedError("Subclasses must implement get_back_url().")

    def get_section_meta(self):
        return self.section_meta

    def get_section_title(self):
        value = getattr(self.object, "label", None)
        if value:
            return value

        return str(self.object)

    def get_section_description(self):
        return None

    def get_edit_button(self):
        return None

    def get_delete_button(self):
        return None

    def get_display_fields(self):
        fields = []

        for label, attr in self.display_field_map:
            value = getattr(self.object, attr, None)

            if value is not None:
                fields.append(
                    self.build_text_field(label, value)
                )

        return fields

    def get_status_badges(self):
        badges = []

        if hasattr(self.object, "is_active"):
            badges.append(
                self.build_badge(
                    label="Estado",
                    value="Activo" if self.object.is_active else "Inactivo",
                    style="success" if self.object.is_active else "danger",
                )
            )

        if hasattr(self.object, "is_required"):
            badges.append(
                self.build_badge(
                    label="Requerido",
                    value="Requerido" if self.object.is_required else "No requerido",
                    style="primary" if self.object.is_required else "secondary",
                )
            )

        if hasattr(self.object, "is_repeatable"):
            badges.append(
                self.build_badge(
                    label="Repetibilidad",
                    value="Repetible" if self.object.is_repeatable else "No repetible",
                    style="warning",
                )
            )

        return badges

    def get_additional_section(self):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "back_url": self.get_back_url(),
            "section_meta": self.get_section_meta(),
            "section_title": self.get_section_title(),
            "section_description": self.get_section_description(),
            "edit_button": self.get_edit_button(),
            "delete_button": self.get_delete_button(),
            "display_fields": self.get_display_fields(),
            "status_badges": self.get_status_badges(),
            "additional_section": self.get_additional_section(),
        })
        
        return context


