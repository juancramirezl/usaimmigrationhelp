from django.views.generic.edit import UpdateView


class BaseGenericUpdateView(UpdateView):
    template_name = "generic/form.html"
    page_title = "Actualizar"

    def get_page_title(self):
        return self.page_title

    def get_back_url(self):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["section_title"] = self.get_page_title()
        context["back_url"] = self.get_back_url()

        return context