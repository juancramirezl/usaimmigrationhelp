from django.urls import reverse_lazy, reverse

from .base.create import BaseGenericCreateView
from .base.detail import BaseGenericDetailView
from .base.update import BaseGenericUpdateView
from .base.delete import BaseGenericDeleteView
from ..models import QuestionGroup
    

FORMSECTION_FIELDS = [
    "question",
    "label",
    "key",
    "order",
    "min_items",
    "max_items",
    "is_required",
    "is_active",
    "is_repeatable",
]


class QuestionGroupCreateView(BaseGenericCreateView):
    model = QuestionGroup
    fields = FORMSECTION_FIELDS
    page_title = "Crear Grupo de Preguntas"
    parent_field_name = "question"
    parent_kwarg_name = "sectionquestion_id"

    def get_back_url(self):
        return reverse_lazy(
            "sectionquestion_detail",
            kwargs={"pk": self.kwargs["sectionquestion_id"]},
        )

    def get_success_url(self):
        return reverse_lazy(
            "sectionquestion_detail",
            kwargs={"pk": self.object.question.pk},
        )
    

class QuestionGroupDetailView(BaseGenericDetailView):
    model = QuestionGroup
    section_meta = "Grupo de Preguntas"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("fields")
    
    # Generic Behavior and Params
    def get_back_url(self):
        return reverse(
            "sectionquestion_detail",
            kwargs={"pk": self.object.question.pk},
        )
    
    def get_section_description(self):
        return f"Pregunta: {self.object.question}"

    def get_edit_button(self):
        return {
            "label": "Grupo",
            "url": reverse("questiongroup_update", kwargs={"pk": self.object.pk}),
        }

    def get_delete_button(self):
        return {
            "label": "Grupo",
            "url": reverse("questiongroup_delete", kwargs={"pk": self.object.pk}),
        }

    def get_display_fields(self):
        fields = super().get_display_fields()
        fields.append({"label": "Mínimo de selecciones", "value": self.object.min_items})
        fields.append({
            "label": "Máximo de selecciones",
            "value": self.object.max_items if self.object.max_items else "Sin Límite",
        })
        return fields
    
    def get_additional_section(self):
        return self.build_default_accordion_section(
            title="Campos del Grupo",
            objects=self.object.fields.all(),
            accordion_id="groupFieldsAccordion",
            detail_url_name="groupfield_detail",
            create_url_name="groupfield_create",
            create_url_kwargs={"questiongroup_id": self.object.pk},
            create_label="Nuevo Campo",
            empty_message="Este grupo aún no tiene campos.",
        )
    

class QuestionGroupUpdateView(BaseGenericUpdateView):
    model = QuestionGroup
    fields = FORMSECTION_FIELDS
    page_title = "Actualizar Grupo de Preguntas"

    def get_back_url(self):
        return reverse(
            "questiongroup_detail",
            kwargs={"pk": self.object.pk},
        )

    def get_success_url(self):
        return reverse(
            "questiongroup_detail",
            kwargs={"pk": self.object.pk},
        )
    
    
class QuestionGroupDeleteView(BaseGenericDeleteView):
    model = QuestionGroup
    page_title = "Eliminar Grupo de Preguntas"

    def get_back_url(self):
        return reverse(
            "questiongroup_detail",
            kwargs={"pk": self.object.pk},
        )

    def get_success_url(self):
        return reverse(
            "sectionquestion_detail",
            kwargs={"pk": self.object.question.pk},
        )

    def get_warning_text(self):
        return "Al eliminar este grupo, se perderá su configuración asociada."

    def get_summary_title(self):
        return "Información General del Grupo"

    def get_confirmation_text(self):
        return "¿Estás seguro de que deseas eliminar este grupo?"