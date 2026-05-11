from shared.views.detail import BaseGenericDetailView
from shared.ui.sections.display import DisplayFieldConfig
from shared.ui.sections.status import StatusBadgeConfig
from shared.ui.sections.table import TableField



class BaseQuestionBankDetailView(BaseGenericDetailView):
    display_fields = (
        DisplayFieldConfig("Orden", "order"),
    )

    status_badges = (
        StatusBadgeConfig(
            label="Estado",
            attr="is_active",
            true_value="Activo",
            false_value="Inactivo",
            true_style="success",
            false_style="danger",
        ),
        StatusBadgeConfig(
            label="Repetibilidad",
            attr="is_repeatable",
            true_value="Repetible",
            false_value="No repetible",
            true_style="warning",
            false_style="secondary",
        ),
    )

    table_fields = (
        TableField("Orden", "order"),
        TableField("Nombre", "label"),
        TableField("Estado", "is_active", "status"),
    )

    def get_section_title(self):
        value = getattr(self.object, "label", None)
        if value:
            return value

        return str(self.object)