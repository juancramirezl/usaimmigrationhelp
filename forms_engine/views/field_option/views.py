from django.urls import reverse

from ..base.create import BaseGenericCreateView
from ..base.detail import BaseGenericDetailView
from ..base.update import BaseGenericUpdateView
from ..base.delete import BaseGenericDeleteView
from ...models import FieldOption


FORMSECTION_FIELDS = ["label", "key", "order", "value", "is_active"]


class FieldOptionCreateView(BaseGenericCreateView):
    model = FieldOption
    fields = FORMSECTION_FIELDS

    page_title = "Crear Opción"
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