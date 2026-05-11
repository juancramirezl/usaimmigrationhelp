from django.views.generic.edit import UpdateView

from ..ui.template_context import EditTemplateContextMixin


class BaseGenericUpdateView(
    EditTemplateContextMixin,
    UpdateView
):
    template_name = "generic/form.html"
    section_title = "Actualizar"