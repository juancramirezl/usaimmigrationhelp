from django.views.generic import CreateView
from django.core.exceptions import ValidationError


class BaseGenericCreateView(CreateView):
    template_name = "generic/form.html"
    page_title = "Crear"

    parent_field_name = None
    parent_kwarg_name = None

    back_url = None

    def get_page_title(self):
        return self.page_title

    def get_back_url(self):
        return self.back_url

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

        # PAGE DATA
        context["section_title"] = self.get_page_title()

        # BACK BUTTON
        context["back_url"] = self.get_back_url()

        # OPTIONAL PARENT ID
        if self.parent_kwarg_name:
            context[self.parent_kwarg_name] = self.get_parent_id()

        return context