from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class ParentScopedOrderMixin(models.Model):
    class Meta:
        abstract = True

    MIN_ORDER = 1

    ORDER_ERROR_MESSAGES = {
        "min_order": "El orden mínimo permitido es 1.",
        "duplicate_order": "Este 'orden' ya está siendo utilizado por otro objeto.",
    }

    order = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                MIN_ORDER,
                message=ORDER_ERROR_MESSAGES["min_order"],
            )
        ],
        help_text="Define la posición de este elemento dentro de su grupo.",
    )

    def get_parent_filter(self):
        raise NotImplementedError("Subclasses must implement get_parent_filter().")

    def get_error_message(self, key):
        return self.ORDER_ERROR_MESSAGES[key]

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
        errors.update(self._validate_order_uniqueness(siblings_qs))

        if errors:
            raise ValidationError(errors)

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
    

class Basemodel(models.Model):
    class Meta:
        abstract = True

    label = models.CharField(
        max_length=255,
        help_text="Texto visible para el usuario. Se mostrará como título o pregunta en la interfaz.",
    )
    is_active = models.BooleanField(
        default=False,
        help_text="Define si este elemento está activo y debe ser utilizado.",
    )

    def __str__(self):
        return self.label