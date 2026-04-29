from django.urls import reverse

from ..base.create import BaseGenericCreateView
from ..base.detail import BaseGenericDetailView
from ..base.update import BaseGenericUpdateView
from ..base.delete import BaseGenericDeleteView
from ...models import SectionQuestion


FORMSECTION_FIELDS = ["label", "key", "order", "is_required", "is_active"]


class SectionQuestionCreateView(BaseGenericCreateView):
    model = SectionQuestion
    fields = FORMSECTION_FIELDS
    page_title = "Crear Pregunta"
    parent_field_name = "section"
    parent_kwarg_name = "formsection_id"

    def get_back_url(self):
        return reverse(
            "formsection_detail",
            kwargs={"pk": self.kwargs["formsection_id"]},
        )

    def get_success_url(self):
        return reverse(
            "formsection_detail",
            kwargs={"pk": self.object.section.pk},
        )
    

class SectionQuestionDetailView(BaseGenericDetailView):
    model = SectionQuestion
    section_meta = "Pregunta de Sección"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("groups")
    
    # Generic Behavior and Params
    def get_back_url(self):
        return reverse(
            "formsection_detail",
            kwargs={"pk": self.object.section.pk},
        )
    
    def get_section_description(self):
        return f"Sección: {self.object.section}"

    def get_edit_button(self):
        return {
            "label": "Pregunta",
            "url": reverse("sectionquestion_update", kwargs={"pk": self.object.pk}),
        }

    def get_delete_button(self):
        return {
            "label": "Pregunta",
            "url": reverse("sectionquestion_delete", kwargs={"pk": self.object.pk}),
        }
    
    def get_additional_section(self):
        return self.build_default_accordion_section(
            title="Grupos de Preguntas",
            objects=self.object.groups.all(),
            accordion_id="groupsAccordion",
            detail_url_name="questiongroup_detail",
            create_url_name="questiongroup_create",
            create_url_kwargs={"sectionquestion_id": self.object.pk},
            create_label="Nuevo Grupo de Preguntas",
            empty_message="Esta pregunta aún no tiene grupos.",
        )
    

class SectionQuestionUpdateView(BaseGenericUpdateView):
    model = SectionQuestion
    fields = FORMSECTION_FIELDS
    page_title = "Actualizar Pregunta"

    def get_back_url(self):
        return reverse(
            "sectionquestion_detail",
            kwargs={"pk": self.object.pk},
        )

    def get_success_url(self):
        return reverse(
            "sectionquestion_detail",
            kwargs={"pk": self.object.pk},
        )


class SectionQuestionDeleteView(BaseGenericDeleteView):
    model = SectionQuestion
    page_title = "Eliminar Pregunta"

    def get_back_url(self):
        return reverse(
            "sectionquestion_detail",
            kwargs={"pk": self.object.pk},
        )

    def get_success_url(self):
        return reverse(
            "formsection_detail",
            kwargs={"pk": self.object.section.pk},
        )

    def get_warning_text(self):
        return "Al eliminar esta pregunta, también se eliminarán todos los grupos relacionados."

    def get_summary_title(self):
        return "Información General de la Pregunta"

    def get_confirmation_text(self):
        return "¿Estás seguro de que deseas eliminar esta pregunta?"