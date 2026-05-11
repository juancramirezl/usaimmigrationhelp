from django.urls import reverse

from shared.views.create import BaseGenericCreateView
from shared.views.update import BaseGenericUpdateView

from .base.detail import BaseQuestionBankDetailView
from .base.delete import BaseQuestionBankDeleteView
from ..models import FieldOption


FORMSECTION_FIELDS = [
    "label",
    "order", 
    "value", 
    "is_active"
]


class FieldOptionCreateView(BaseGenericCreateView):
    model = FieldOption
    fields = FORMSECTION_FIELDS

    section_title = "Crear Opción"
    parent_field_name = "field"
    parent_kwarg_name = "groupfield_id"

    def get_back_url(self):
        return reverse(
            "groupfield_detail",
            kwargs={"pk": self.kwargs["groupfield_id"]},
        )

    def get_success_url(self):
        return reverse(
            "groupfield_detail",
            kwargs={"pk": self.object.field.pk},
        )
    

class FieldOptionDetailView(BaseQuestionBankDetailView):
    model = FieldOption
    section_meta = "Opción de Campo"
    object_update_url_name = "fieldoption_update"
    object_delete_url_name = "fieldoption_delete"

    def get_back_url(self):
        return reverse(
            "groupfield_detail",
            kwargs={"pk": self.object.field.pk},
        )

    def get_section_description(self):
        return f"Campo de Grupo: {self.object.field}"
    

class FieldOptionUpdateView(BaseGenericUpdateView):
    model = FieldOption
    fields = FORMSECTION_FIELDS
    section_title = "Actualizar Campo"

    def get_back_url(self):
        return reverse(
            "fieldoption_detail",
            kwargs={"pk": self.object.pk},
        )

    def get_success_url(self):
        return reverse(
            "fieldoption_detail",
            kwargs={"pk": self.object.pk},
        )


class FieldOptionDeleteView(BaseQuestionBankDeleteView):
    model = FieldOption
    section_title = "Eliminar Opción de Campo"

    def get_back_url(self):
        return reverse(
            "fieldoption_detail",
            kwargs={"pk": self.object.pk},
        )

    def get_success_url(self):
        return reverse(
            "groupfield_detail",
            kwargs={"pk": self.object.field.pk},
        )