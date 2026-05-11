from django.views.generic import DeleteView

from ..ui.template_context import EditTemplateContextMixin
from ..ui.styling.fields import UIFieldBuilderMixin


class BaseGenericDeleteView(
    UIFieldBuilderMixin,
    EditTemplateContextMixin, 
    DeleteView
):
    template_name = "generic/delete_form.html"
    section_title = "Eliminar"

    warning_text = None
    summary_title = None
    confirmation_text = None
    cancel_label = None
    confirm_label = None
    
    summary_display_fields = ()
    summary_status_badges = ()

    def get_warning_text(self):
        return self.warning_text

    def get_summary_title(self):
        return self.summary_title
    
    def get_confirmation_text(self):
        return self.confirmation_text
    
    def get_cancel_label(self):
        return self.cancel_label

    def get_confirm_label(self):
        return self.confirm_label
    
    def get_summary_display_fields_config(self):
        return self.summary_display_fields

    def get_summary_status_badges_config(self):
        return self.summary_status_badges

    def get_summary_display_fields(self):
        fields = []

        for config in self.get_summary_display_fields_config():
            field = self.build_display_field(config)

            if field:
                fields.append(field)

        return fields

    def get_summary_status_badges(self):
        badges = []

        for config in self.get_summary_status_badges_config():
            badge = self.build_status_badge(config)

            if badge:
                badges.append(badge)

        return badges

    def get_summary_fields(self):
        return [
            *self.get_summary_display_fields(),
            *self.get_summary_status_badges(),
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["warning_text"] = self.get_warning_text()
        context["summary_title"] = self.get_summary_title()
        context["summary_fields"] = self.get_summary_fields()
        context["confirmation_text"] = self.get_confirmation_text()
        context["cancel_label"] = self.get_cancel_label()
        context["confirm_label"] = self.get_confirm_label()
        return context