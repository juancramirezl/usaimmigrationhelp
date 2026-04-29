from django.urls import reverse_lazy, reverse

import django_countries as djc
from localflavor.us.us_states import USPS_CHOICES

from ..base.create import BaseGenericCreateView
from ..base.detail import BaseGenericDetailView
from ..base.update import BaseGenericUpdateView
from ..base.delete import BaseGenericDeleteView
from ...models import GroupField
    

FORMSECTION_FIELDS = [
    "label",
    "key",
    "order",
    "field_type",
    "option_source",
    "is_required",
    "is_active",
]


class GroupFieldCreateView(BaseGenericCreateView):
    model = GroupField
    fields = FORMSECTION_FIELDS
    page_title = "Crear Campo de Pregunta"
    parent_field_name = "group"
    parent_kwarg_name = "questiongroup_id"

    def get_back_url(self):
        return reverse_lazy(
            "questiongroup_detail",
            kwargs={"pk": self.kwargs["questiongroup_id"]},
        )

    def get_success_url(self):
        return reverse_lazy(
            "questiongroup_detail",
            kwargs={"pk": self.object.group.pk},
        )
    
    
class GroupFieldDetailView(BaseGenericDetailView):
    model = GroupField
    section_meta = "Campo de Grupo de Pregunta"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("options")
    
    # Generic Behavior and Params
    def get_back_url(self):
        return reverse(
            "questiongroup_detail",
            kwargs={"pk": self.object.group.pk},
        )
    
    def get_section_description(self):
        return f"Grupo de Pregunta: {self.object.group}"

    def get_edit_button(self):
        return {
            "label": "Campo",
            "url": reverse("groupfield_update", kwargs={"pk": self.object.pk}),
        }

    def get_delete_button(self):
        return {
            "label": "Campo",
            "url": reverse("groupfield_delete", kwargs={"pk": self.object.pk}),
        }

    def get_display_fields(self):
        fields = super().get_display_fields()

        fields.extend([
            {
                "label": "Tipo de Campo",
                "value": self.object.get_field_type_display(),
            },
            {
                "label": "Fuente de Respuesta del Campo",
                "value": self.object.get_option_source_display(),
            },
        ])

        return fields
    
    def get_additional_section(self):
        if self.object.field_type != "select":
            return None

        if self.object.option_source == "db":
            return self.get_database_options_section()

        if self.object.option_source == "countries":
            return self.get_countries_section()

        if self.object.option_source == "us_states":
            return self.get_us_states_section()

        return None

    def get_database_options_section(self):
        return self.build_default_accordion_section(
            title="Opciones en Base de Datos",
            objects=self.object.options.all(),
            accordion_id="groupFieldOptionsAccordion",
            detail_url_name=None,
            create_url_name="fileoption_create",
            create_url_kwargs={"groupfield_id": self.object.pk},
            create_label="Nueva Opción",
            empty_message="Este campo aún no tiene opciones.",
        )

    def get_countries_section(self):
        return self.build_default_list_section(
            title="Países Disponibles",
            choices=djc.countries,
            page_param="countries_page",
            empty_message="No hay países disponibles.",
        )

    def get_us_states_section(self):
        return self.build_default_list_section(
            title="Estados de EE.UU. Disponibles",
            choices=USPS_CHOICES,
            page_param="states_page",
            empty_message="No hay estados disponibles.",
        )


class GroupFieldUpdateView(BaseGenericUpdateView):
    model = GroupField
    fields = FORMSECTION_FIELDS
    page_title = "Actualizar Campo"

    def get_back_url(self):
        return reverse(
            "groupfield_detail",
            kwargs={"pk": self.object.pk},
        )

    def get_success_url(self):
        return reverse(
            "groupfield_detail",
            kwargs={"pk": self.object.pk},
        )


class GroupFieldDeleteView(BaseGenericDeleteView):
    model = GroupField
    page_title = "Eliminar Campo"

    def get_back_url(self):
        return reverse(
            "groupfield_detail",
            kwargs={"pk": self.object.pk},
        )

    def get_success_url(self):
        return reverse(
            "questiongroup_detail",
            kwargs={"pk": self.object.group.pk},
        )

    def get_warning_text(self):
        return "Al eliminar este campo, también se eliminarán todas las opciones relacionadas."

    def get_summary_title(self):
        return "Información General del Campo"

    def get_confirmation_text(self):
        return "¿Estás seguro de que deseas eliminar este campo?"