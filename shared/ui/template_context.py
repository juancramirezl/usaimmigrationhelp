class TemplateContextMixin:
    section_meta = None
    section_title = None
    section_description = None
    back_url = None
    section_width = "col-12 col-lg-11 col-xl-10"

    def get_back_url(self):
        return self.back_url

    def get_section_meta(self):
        return self.section_meta

    def get_section_title(self):
        return self.section_title

    def get_section_description(self):
        return self.section_description

    def get_section_width(self):
        return self.section_width

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "back_url": self.get_back_url(),
            "section_meta": self.get_section_meta(),
            "section_title": self.get_section_title(),
            "section_description": self.get_section_description(),
            "section_width": self.get_section_width(),
        })

        return context
    

class EditTemplateContextMixin(TemplateContextMixin):
    section_width = "col-12 col-md-9 col-lg-7 col-xl-6"