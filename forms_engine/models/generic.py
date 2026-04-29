from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class OrderedScopedKeyMixin(models.Model):
    class Meta:
        abstract = True

    MIN_ORDER = 1

    ERROR_MESSAGES = {
        "min_order": "El orden mínimo permitido es 1.",
        "duplicate_key": "Esta 'key' ya existe para este grupo.",
        "duplicate_order": "Este 'orden' ya está siendo utilizado por otro objeto.",
    }

    label = models.CharField(
        max_length=255,
        help_text="Texto visible para el usuario. Se mostrará como título o pregunta en la interfaz.",
    )

    key = models.CharField(
        max_length=100,
        help_text="Identificador interno (no visible al usuario). Ej: 'personal_data'.",
    )

    is_active = models.BooleanField(
        default=False,
        help_text="Define si este elemento está activo y debe ser utilizado.",
    )

    order = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                MIN_ORDER,
                message=ERROR_MESSAGES["min_order"],
            )
        ],
        help_text="Define la posición de este elemento dentro de su grupo.",
    )

    def get_parent_filter(self):
        raise NotImplementedError("Subclasses must implement get_parent_filter().")

    def get_error_message(self, key):
        return self.ERROR_MESSAGES[key]

    def clean(self):
        super().clean()

        parent_filter = self.get_parent_filter()
        if not parent_filter:
            return

        siblings_qs = (
            self.__class__.objects
            .filter(**parent_filter)
            .exclude(pk=self.pk)
        )

        errors = {}
        errors.update(self._validate_key_uniqueness(siblings_qs))
        errors.update(self._validate_order_uniqueness(siblings_qs))

        if errors:
            raise ValidationError(errors)

    def _validate_key_uniqueness(self, siblings_qs):
        if self.key and siblings_qs.filter(key=self.key).exists():
            return {
                "key": self.get_error_message("duplicate_key")
            }
        return {}

    def _validate_order_uniqueness(self, siblings_qs):
        if (
            self.is_active
            and self.order is not None
            and siblings_qs.filter(order=self.order, is_active=True).exists()
        ):
            return {
                "order": self.get_error_message("duplicate_order")
            }
        return {}