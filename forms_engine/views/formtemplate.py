from django.urls import reverse_lazy, reverse
from django.views.generic.list import ListView

from .base.create import BaseGenericCreateView
from .base.detail import BaseGenericDetailView
from .base.update import BaseGenericUpdateView
from .base.delete import BaseGenericDeleteView

from ..models import FormTemplate


FORMSECTION_FIELDS = "__all__"


class FormTemplateListView(ListView):
    template_name = "forms_engine/formtemplate/list.html"
    model = FormTemplate
    paginate_by = 15


class FormTemplateCreateView(BaseGenericCreateView):
    model = FormTemplate
    fields = FORMSECTION_FIELDS
    page_title = "Crear Plantilla"

    def get_back_url(self):
        return reverse_lazy("formtemplate_list")

    def get_success_url(self):
        return reverse_lazy("formtemplate_list")


class FormTemplateDetailView(BaseGenericDetailView):
    model = FormTemplate
    section_meta = "Plantilla de Forma"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("sections")
    
    # Generic Behavior and Params
    def get_back_url(self):
        return reverse("formtemplate_list")
    
    def get_section_description(self):
        return None

    def get_edit_button(self):
        return {
            "label": "Plantilla",
            "url": reverse("formtemplate_update", kwargs={"pk": self.object.pk}),
        }

    def get_delete_button(self):
        return {
            "label": "Plantilla",
            "url": reverse("formtemplate_delete", kwargs={"pk": self.object.pk}),
        }

    def get_display_fields(self):
        return [
            {"label": "Código de Forma", "value": self.object.form_code},
        ]
    
    def get_additional_section(self):
        return self.build_default_accordion_section(
            title="Secciones de la Plantilla",
            objects=self.object.sections.all(),
            accordion_id="sectionsAccordion",
            detail_url_name="formsection_detail",
            create_url_name="formsection_create",
            create_url_kwargs={"formtemplate_id": self.object.pk},
            create_label="Agregar Sección",
            empty_message="No hay secciones registradas para esta plantilla.",
        )
    

class FormTemplateUpdateView(BaseGenericUpdateView):
    model = FormTemplate
    fields = FORMSECTION_FIELDS
    page_title = "Actualizar Plantilla"

    def get_back_url(self):
        return reverse(
            "formtemplate_detail",
            kwargs={"pk": self.object.pk},
        )

    def get_success_url(self):
        return reverse(
            "formtemplate_detail",
            kwargs={"pk": self.object.pk},
        )
    

class FormTemplateDeleteView(BaseGenericDeleteView):
    model = FormTemplate
    page_title = "Eliminar Plantilla"
    summary_field_map = (
        ("Nombre", "label"),
        ("Código", "form_code"),
    )

    def get_back_url(self):
        return reverse(
            "formtemplate_detail",
            kwargs={"pk": self.object.pk},
        )

    def get_success_url(self):
        return reverse_lazy("formtemplate_list")

    def get_warning_text(self):
        return "Al eliminar esta plantilla, también se eliminarán todas sus secciones, preguntas y grupos relacionados."

    def get_summary_title(self):
        return "Información General de la Plantilla"

    def get_confirmation_text(self):
        return "¿Estás seguro de que deseas eliminar esta plantilla?"