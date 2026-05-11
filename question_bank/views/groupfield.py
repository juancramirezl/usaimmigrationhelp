from django.urls import reverse

import django_countries as djc
from localflavor.us.us_states import USPS_CHOICES

from shared.views.create import BaseGenericCreateView
from shared.views.update import BaseGenericUpdateView
from shared.ui.sections.display import DisplayFieldConfig

from .base.detail import BaseQuestionBankDetailView
from .base.delete import BaseQuestionBankDeleteView
from ..models import GroupField
    

FORMSECTION_FIELDS = [
    "label",
    "order",
    "field_type",
    "option_source",
    "is_active",
]


class GroupFieldCreateView(BaseGenericCreateView):
    model = GroupField
    fields = FORMSECTION_FIELDS
    section_title = "Crear Campo de Pregunta"
    parent_field_name = "group"
    parent_kwarg_name = "questiongroup_id"

    def get_back_url(self):
        return reverse(
            "questiongroup_detail",
            kwargs={"pk": self.kwargs["questiongroup_id"]},
        )

    def get_success_url(self):
        return reverse(
            "questiongroup_detail",
            kwargs={"pk": self.object.group.pk},
        )
    
    
class GroupFieldDetailView(BaseQuestionBankDetailView):
    model = GroupField
    section_meta = "Campo de Grupo de Pregunta"
    object_update_url_name = "groupfield_update"
    object_delete_url_name = "groupfield_delete"

    display_fields = BaseQuestionBankDetailView.display_fields + (
    DisplayFieldConfig("Tipo de Campo", "get_field_type_display"),
    DisplayFieldConfig("Fuente de Respuesta del Campo", "get_option_source_display"),
)

    def get_queryset(self):
        return super().get_queryset().prefetch_related("options")
    
    def get_back_url(self):
        return reverse(
            "questiongroup_detail",
            kwargs={"pk": self.object.group.pk},
        )
    
    def get_section_description(self):
        return f"Grupo de Pregunta: {self.object.group}"
    
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
        return self.build_default_table_section(
            title="Opciones en Base de Datos",
            objects=self.object.options.all(),
            detail_url_name="fieldoption_detail",
            update_url_name=None,
            create_url_name="fieldoption_create",
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
    section_title = "Actualizar Campo"

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


class GroupFieldDeleteView(BaseQuestionBankDeleteView):
    model = GroupField
    section_title = "Eliminar Campo"
    warning_text = "Al eliminar este campo, también se eliminarán todas las opciones relacionadas."

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