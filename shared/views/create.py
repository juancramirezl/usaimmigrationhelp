from django.views.generic import CreateView
from django.core.exceptions import ValidationError

from ..ui.template_context import EditTemplateContextMixin


class BaseGenericCreateView(
    EditTemplateContextMixin,
    CreateView
):
    template_name = "generic/form.html"
    section_title = "Crear"

    parent_field_name = None
    parent_kwarg_name = None

    def get_parent_id(self):
        if self.parent_kwarg_name:
            return self.kwargs.get(self.parent_kwarg_name)
        return None

    def assign_parent(self, form):
        if self.parent_field_name and self.parent_kwarg_name:
            setattr(
                form.instance,
                f"{self.parent_field_name}_id",
                self.get_parent_id()
            )

    def form_valid(self, form):
        self.assign_parent(form)

        try:
            form.instance.full_clean()
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    form.add_error(field, error)
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.parent_kwarg_name:
            context[self.parent_kwarg_name] = self.get_parent_id()

        return context