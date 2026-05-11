from django.urls import reverse

from shared.views.create import BaseGenericCreateView
from shared.views.update import BaseGenericUpdateView

from .base.detail import BaseQuestionBankDetailView, DisplayFieldConfig
from .base.delete import BaseQuestionBankDeleteView
from ..models import QuestionGroup
    

FORMSECTION_FIELDS = [
    "label",
    "order",
    "min_items",
    "max_items",
    "is_active",
    "is_repeatable",
]


class QuestionGroupCreateView(BaseGenericCreateView):
    model = QuestionGroup
    fields = FORMSECTION_FIELDS
    section_title = "Crear Grupo de Preguntas"
    parent_field_name = "question"
    parent_kwarg_name = "question_id"

    def get_back_url(self):
        return reverse(
            "question_detail",
            kwargs={"pk": self.kwargs["question_id"]},
        )

    def get_success_url(self):
        return reverse(
            "question_detail",
            kwargs={"pk": self.object.question.pk},
        )
    

class QuestionGroupDetailView(BaseQuestionBankDetailView):
    model = QuestionGroup
    section_meta = "Grupo de Preguntas"
    object_update_url_name = "questiongroup_update"
    object_delete_url_name = "questiongroup_delete"

    display_fields = BaseQuestionBankDetailView.display_fields + (
        DisplayFieldConfig("Mínimo de selecciones", "min_items"),
        DisplayFieldConfig("Máximo de selecciones", "max_items"),
    )

    def get_queryset(self):
        return super().get_queryset().prefetch_related("fields")
    
    def get_back_url(self):
        return reverse(
            "question_detail",
            kwargs={"pk": self.object.question.pk},
        )
    
    def get_section_description(self):
        return f"Pregunta: {self.object.question}"

    def get_additional_section(self):
        return self.build_default_table_section(
            title="Campos del Grupo",
            objects=self.object.fields.all(),
            detail_url_name="groupfield_detail",
            # update_url_name="groupfield_update",
            create_url_name="groupfield_create",
            create_url_kwargs={"questiongroup_id": self.object.pk},
            create_label="Nuevo Campo",
            empty_message="Este grupo aún no tiene campos.",
        )
    

class QuestionGroupUpdateView(BaseGenericUpdateView):
    model = QuestionGroup
    fields = FORMSECTION_FIELDS
    section_title = "Actualizar Grupo de Preguntas"

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
    
    
class QuestionGroupDeleteView(BaseQuestionBankDeleteView):
    model = QuestionGroup
    section_title = "Eliminar Grupo de Preguntas"
    warning_text = "Al eliminar este grupo, se perderá su configuración asociada."

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