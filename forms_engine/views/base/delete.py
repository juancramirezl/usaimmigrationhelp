from django.views.generic import DeleteView

from .ui import StyleBuilderMixin


class BaseGenericDeleteView(StyleBuilderMixin, DeleteView):
    template_name = "generic/delete_form.html"
    page_title = "Eliminar"
    confirm_label = "Sí, Eliminar"
    summary_field_map = (
        ("Nombre", "label"),
        ("Clave", "key"),
    )

    def get_page_title(self):
        return self.page_title

    def get_back_url(self):
        return None

    def get_warning_title(self):
        return "Esta acción no se puede deshacer."

    def get_warning_text(self):
        return ""

    def get_summary_title(self):
        return "Información General"
    
    def get_summary_fields(self):
        fields = []

        for label, attr in getattr(self, "summary_field_map", []):
            value = getattr(self.object, attr, None)
            if value:
                fields.append(self.build_text_field(label, value))

        if hasattr(self.object, "is_active"):
            fields.append(
                self.build_badge_field(
                    "Estado",
                    "Activo" if self.object.is_active else "Inactivo",
                    style="success" if self.object.is_active else "danger",
                )
            )

        return fields

    def get_confirmation_text(self):
        return "¿Estás seguro de que deseas continuar?"

    def get_cancel_label(self):
        return "Cancelar"

    def get_confirm_label(self):
        return self.confirm_label

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["section_title"] = self.get_page_title()
        context["back_url"] = self.get_back_url()
        context["warning_title"] = self.get_warning_title()
        context["warning_text"] = self.get_warning_text()
        context["summary_title"] = self.get_summary_title()
        context["summary_fields"] = self.get_summary_fields()
        context["confirmation_text"] = self.get_confirmation_text()
        context["cancel_label"] = self.get_cancel_label()
        context["confirm_label"] = self.get_confirm_label()
        return context