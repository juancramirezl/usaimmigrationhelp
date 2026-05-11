class UIIconMixin:
    ICONS = {
        "edit": "bi bi-pencil-fill",
        "delete": "bi bi-trash-fill",
        "add": "bi bi-plus-circle-fill",
        "view": "bi bi-eye-fill",
        "back": "bi bi-arrow-left",
    }

    def get_icon_class(self, icon=None):
        if not icon:
            return None

        return self.ICONS.get(icon)