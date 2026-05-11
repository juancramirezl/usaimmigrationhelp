from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView

from shared.views.create import BaseGenericCreateView
from shared.views.update import BaseGenericUpdateView

from .base.detail import BaseQuestionBankDetailView
from .base.delete import BaseQuestionBankDeleteView
from ..models import Question


FORMSECTION_FIELDS = "__all__"


class FormTemplateListView(ListView):
    template_name = "question_bank/generic/list.html"
    model = Question
    paginate_by = 15


class QuestionCreateView(BaseGenericCreateView):
    model = Question
    fields = FORMSECTION_FIELDS
    section_title = "Crear Pregunta"
    success_url = reverse_lazy("question_list")
    back_url = reverse_lazy("question_list")


class QuestionDetailView(BaseQuestionBankDetailView):
    model = Question
    back_url = reverse_lazy("question_list")
    section_meta = "Pregunta"
    object_update_url_name = "question_update"
    object_delete_url_name = "question_delete"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("groups")
    
    def get_additional_section(self):
        return self.build_default_table_section(
            title="Grupos de Preguntas",
            objects=self.object.groups.all(),
            detail_url_name="questiongroup_detail",
            # update_url_name="questiongroup_update",
            create_url_name="questiongroup_create",
            create_url_kwargs={"question_id": self.object.pk},
            create_label="Nuevo Grupo de Preguntas",
            empty_message="Esta pregunta aún no tiene grupos.",
        )
    

class QuestionUpdateView(BaseGenericUpdateView):
    model = Question
    fields = FORMSECTION_FIELDS
    section_title = "Actualizar Pregunta"

    def get_back_url(self):
        return reverse(
            "question_detail",
            kwargs={"pk": self.object.pk},
        )

    def get_success_url(self):
        return reverse(
            "question_detail",
            kwargs={"pk": self.object.pk},
        )


class QuestionDeleteView(BaseQuestionBankDeleteView):
    model = Question
    success_url = reverse_lazy("question_list")
    section_title = "Eliminar Pregunta"
    warning_text = "Al eliminar esta pregunta, también se eliminarán todos los grupos relacionados."

    def get_back_url(self):
        return reverse(
            "question_detail",
            kwargs={"pk": self.object.pk},
        )