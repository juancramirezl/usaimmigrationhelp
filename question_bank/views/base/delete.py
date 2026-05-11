from shared.views.delete import BaseGenericDeleteView
from shared.ui.sections.display import DisplayFieldConfig
from shared.ui.sections.status import StatusBadgeConfig


class BaseQuestionBankDeleteView(BaseGenericDeleteView):
    summary_display_fields = (
        DisplayFieldConfig("Nombre", "label"),
    )
    
    summary_status_badges = (
        StatusBadgeConfig(
            label="Estado",
            attr="is_active",
            true_value="Activo",
            false_value="Inactivo",
            true_style="success",
            false_style="danger",
        ),
    )

