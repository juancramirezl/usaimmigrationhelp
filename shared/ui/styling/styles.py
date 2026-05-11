class UIStyleMixin:
    DEFAULT_STYLE = "secondary"
    DEFAULT_BUTTON_STYLE = "primary"

    UI_STYLES = {
        "success": {
            "badge": "bg-success",
            "button": "btn btn-success",
        },
        "danger": {
            "badge": "bg-danger",
            "button": "btn btn-danger",
        },
        "warning": {
            "badge": "bg-warning",
            "button": "btn btn-warning text-dark",
        },
        "info": {
            "badge": "bg-info text-dark",
            "button": "btn btn-info text-dark",
        },
        "primary": {
            "badge": "bg-primary",
            "button": "btn btn-primary",
        },
        "secondary": {
            "badge": "bg-secondary",
            "button": "btn btn-secondary",
        },
        "dark": {
            "badge": "bg-dark",
            "button": "btn btn-dark",
        },
        "outline-primary": {
            "badge": "bg-primary",
            "button": "btn btn-outline-primary",
        },
        "outline-danger": {
            "badge": "bg-danger",
            "button": "btn btn-outline-danger",
        },
        "outline-secondary": {
            "badge": "bg-secondary",
            "button": "btn btn-outline-secondary",
        },
    }

    def get_ui_class(self, component, style=None):
        style = style or self.DEFAULT_STYLE

        style_config = self.UI_STYLES.get(
            style,
            self.UI_STYLES[self.DEFAULT_STYLE],
        )

        return style_config.get(component, "")