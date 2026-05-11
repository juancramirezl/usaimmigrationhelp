from django.urls import reverse
from django.views.generic import DetailView

from ..ui.styling.buttons import UIButtonBuilderMixin
from ..ui.template_context import TemplateContextMixin
from ..ui.sections.display import DisplayFieldsSectionMixin
from ..ui.sections.status import StatusBadgesSectionMixin
from ..ui.sections.table import TableSectionMixin
from ..ui.sections.list import ListSectionMixin


class ObjectActionMixin(UIButtonBuilderMixin):
    object_update_url_name = None
    object_delete_url_name = None

    def get_object_update_url_name(self):
        return self.object_update_url_name

    def get_object_delete_url_name(self):
        return self.object_delete_url_name

    def get_object_url(self, url_name):
        if not url_name:
            return None

        return reverse(url_name, kwargs={"pk": self.object.pk})

    def get_update_url(self):
        return self.get_object_url(self.get_object_update_url_name())

    def get_delete_url(self):
        return self.get_object_url(self.get_object_delete_url_name())

    def get_action_buttons(self):
        buttons = []

        update_url = self.get_update_url()
        delete_url = self.get_delete_url()

        if update_url:
            buttons.append(self.build_edit_button(url=update_url))

        if delete_url:
            buttons.append(self.build_delete_button(url=delete_url))

        return buttons


class BaseGenericDetailView(
    TemplateContextMixin,
    ObjectActionMixin,
    DisplayFieldsSectionMixin,
    StatusBadgesSectionMixin,
    TableSectionMixin,
    ListSectionMixin,
    DetailView,
):
    template_name = "shared/generic/detail.html"
    
    def get_additional_section(self):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "back_url": self.get_back_url(),
            "section_meta": self.get_section_meta(),
            "section_title": self.get_section_title(),
            "section_description": self.get_section_description(),
            "action_buttons": self.get_action_buttons(),
            "display_section": self.get_display_section(),
            "status_badge_section": self.get_status_badge_section(),
            "additional_section": self.get_additional_section(),
        })
        
        return context


