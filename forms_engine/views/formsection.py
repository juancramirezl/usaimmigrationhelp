from django.urls import reverse

from .base.create import BaseGenericCreateView
from .base.detail import BaseGenericDetailView
from .base.update import BaseGenericUpdateView
from .base.delete import BaseGenericDeleteView
from ..models import FormSection


FORMSECTION_FIELDS = ["label", "key", "order", "is_required", "is_active"]


class FormSectionCreateView(BaseGenericCreateView):
    model = FormSection
    fields = FORMSECTION_FIELDS
    page_title = "Crear Sección"
    parent_field_name = "form_template"
    parent_kwarg_name = "formtemplate_id"

    def get_back_url(self):
        return reverse(
            "formtemplate_detail",
            kwargs={"pk": self.kwargs["formtemplate_id"]},
        )

    def get_success_url(self):
        return reverse(
            "formtemplate_detail",
            kwargs={"pk": self.object.form_template.pk},
        )


class FormSectionDetailView(BaseGenericDetailView):
    model = FormSection
    section_meta = "Sección de Forma"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("questions")
    
    # Generic Behavior and Params
    def get_back_url(self):
        return reverse(
            "formtemplate_detail",
            kwargs={"pk": self.object.form_template.pk}
        )
    
    def get_section_description(self):
        return f"Forma: {self.object.form_template}"

    def get_edit_button(self):
        return {
            "label": "Sección",
            "url": reverse("formsection_update", kwargs={"pk": self.object.pk}),
        }

    def get_delete_button(self):
        return {
            "label": "Sección",
            "url": reverse("formsection_delete", kwargs={"pk": self.object.pk}),
        }
    
    def get_additional_section(self):
        return self.build_default_table_section(
            title="Preguntas de la Sección",
            objects=self.object.questions.all(),
            detail_url_name="sectionquestion_detail",
            create_url_name="sectionquestion_create",
            create_url_kwargs={"formsection_id": self.object.pk},
            create_label="Nueva Pregunta",
            empty_message="Esta sección aún no tiene preguntas.",
        )


class FormSectionUpdateView(BaseGenericUpdateView):
    model = FormSection
    fields = FORMSECTION_FIELDS
    page_title = "Actualizar Sección"

    def get_back_url(self):
        return reverse(
            "formsection_detail",
            kwargs={"pk": self.object.pk},
        )

    def get_success_url(self):
        return reverse(
            "formsection_detail",
            kwargs={"pk": self.object.pk},
        )
    

class FormSectionDeleteView(BaseGenericDeleteView):
    model = FormSection
    page_title = "Eliminar Sección"

    def get_back_url(self):
        return reverse("formsection_detail", kwargs={"pk": self.object.pk})

    def get_success_url(self):
        return reverse("formtemplate_detail", kwargs={"pk": self.object.form_template.pk})

    def get_warning_text(self):
        return "Al eliminar esta sección, también se eliminarán todas las preguntas relacionadas."

    def get_summary_title(self):
        return "Información General de la Sección"

    def get_confirmation_text(self):
        return "¿Estás seguro de que deseas eliminar esta sección?"