from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from .base import ParentScopedOrderMixin, Basemodel


class Question(Basemodel):
    pass
    

class QuestionGroup(Basemodel, ParentScopedOrderMixin):
    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["question", "order"],
                condition=Q(is_active=True),
                name="unique_active_group_order_per_question",
            ),
        ]

    NON_REPEATABLE_ITEM_COUNT = 1

    REPEATABILITY_ERROR_MESSAGES = {
        "non_repeatable_min_items": _(
            "Los grupos no repetibles deben tener min_items = 1."
        ),
        "non_repeatable_max_items": _(
            "Los grupos no repetibles deben tener max_items = 1."
        ),
        "repeatable_max_items_one": _(
            "Un grupo repetible no puede tener max_items = 1."
        ),
        "max_items_less_than_min_items": _(
            "max_items no puede ser menor que min_items."
        ),
    }

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="groups",
        help_text="Pregunta a la que pertenece este grupo."
    )
    min_items = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Cantidad mínima de veces que se puede completar este grupo (todos sus campos)."
    )
    max_items = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1, message="La cantidad máxima debe ser al menos 1.",)],
        help_text="Cantidad máxima de veces que se puede completar este grupo. Puede dejarse vacío si no hay límite.",
    )
    is_repeatable = models.BooleanField(
        default=False,
        help_text="Indica si este grupo puede repetirse múltiples veces."
    )

    def get_parent_filter(self):
        if self.question_id:
            return {"question": self.question}
        return {}
    
    def get_repeatability_error_message(self, key):
        return self.REPEATABILITY_ERROR_MESSAGES[key]

    def clean(self):
        super().clean()

        errors = {}
        errors.update(self._get_repeatability_errors())

        if errors:
            raise ValidationError(errors)

    def _get_repeatability_errors(self):
        if self.is_repeatable:
            return self._get_repeatable_group_errors()

        return self._get_non_repeatable_group_errors()

    def _get_non_repeatable_group_errors(self):
        errors = {}

        if self.min_items != self.NON_REPEATABLE_ITEM_COUNT:
            errors["min_items"] = self.get_repeatability_error_message(
                "non_repeatable_min_items"
            )

        if self.max_items != self.NON_REPEATABLE_ITEM_COUNT:
            errors["max_items"] = self.get_repeatability_error_message(
                "non_repeatable_max_items"
            )

        return errors

    def _get_repeatable_group_errors(self):
        errors = {}

        if self.max_items == self.NON_REPEATABLE_ITEM_COUNT:
            errors["max_items"] = self.get_repeatability_error_message(
                "repeatable_max_items_one"
            )

        if self._max_items_is_less_than_min_items():
            errors["max_items"] = self.get_repeatability_error_message(
                "max_items_less_than_min_items"
            )

        return errors

    def _max_items_is_less_than_min_items(self):
        return self.max_items is not None and self.max_items < self.min_items
    

class GroupField(Basemodel, ParentScopedOrderMixin):
    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["group", "order"],
                condition=Q(is_active=True),
                name="unique_active_field_order_per_group",
            ),
        ]

    FIELD_TYPE_ERROR_MESSAGES = {
        "select_requires_option_source": _(
            "Los campos tipo select deben definir una fuente de opciones."
        ),
        "only_select_uses_option_source": _(
            "Solo los campos tipo select pueden definir una fuente de opciones."
        ),
        "locked_field_type": _(
            "No puedes cambiar el tipo de campo porque ya existen opciones asociadas."
        ),
        "locked_option_source": _(
            "No puedes cambiar la fuente de opciones porque ya existen opciones asociadas."
        ),
    }

    FIELD_TYPES = [
        ("text", "Text"),
        ("textarea", "Textarea"),
        ("date", "Date"),
        ("integer", "Integer"),
        ("decimal", "Decimal"),
        ("select", "Select"),
        ("boolean", "Boolean"),
    ]

    OPTION_SOURCES = [
        ("db", "Database"),
        ("countries", "Countries Library"),
        ("us_states", "US States Catalog"),
    ]

    group = models.ForeignKey(
        QuestionGroup,
        on_delete=models.CASCADE,
        related_name="fields",
        help_text="Grupo al que pertenece este campo."
    )
    field_type = models.CharField(
        max_length=20,
        choices=FIELD_TYPES,
        help_text="Tipo de campo que define el comportamiento del input."
    )
    option_source = models.CharField(
        max_length=20,
        choices=OPTION_SOURCES,
        blank=True,
        default="",
        help_text="Fuente de datos para las opciones en campos tipo select."
    )

    def __str__(self):
        return self.label

    def get_parent_filter(self):
        if self.group_id:
            return {"group": self.group}
        return {}
    
    def get_field_type_error_message(self, key):
        return self.FIELD_TYPE_ERROR_MESSAGES[key]

    @property
    def is_select_field(self):
        return self.field_type == "select"

    @property
    def has_option_source(self):
        return bool(self.option_source)

    @property
    def uses_database_options(self):
        return self.option_source == "db"
    
    def clean(self):
        super().clean()

        errors = {}
        errors.update(self._get_option_source_errors())
        errors.update(self._get_locked_option_config_errors())

        if errors:
            raise ValidationError(errors)

    def _get_option_source_errors(self):
        errors = {}

        if self.is_select_field and not self.has_option_source:
            errors["option_source"] = self.get_field_type_error_message(
                "select_requires_option_source"
            )

        if not self.is_select_field and self.has_option_source:
            errors["option_source"] = self.get_field_type_error_message(
                "only_select_uses_option_source"
            )

        return errors
    
    def _get_locked_option_config_errors(self):
        errors = {}

        if not self.pk:
            return errors

        old = self._get_old_instance()

        has_existing_options = old.options.exists()

        if not has_existing_options:
            return errors

        if old.field_type != self.field_type:
            errors["field_type"] = self.get_field_type_error_message(
                "locked_field_type"
            )

        if old.option_source != self.option_source:
            errors["option_source"] = self.get_field_type_error_message(
                "locked_option_source"
            )

        return errors
    
    def _get_old_instance(self):
        return type(self).objects.get(pk=self.pk)


class FieldOption(Basemodel, ParentScopedOrderMixin):
    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["field", "order"],
                condition=Q(is_active=True),
                name="unique_active_option_order_per_field",
            ),
        ]

    field = models.ForeignKey(
        GroupField,
        on_delete=models.CASCADE,
        related_name="options",
        help_text="Campo al que pertenece esta opción."
    )
    value = models.CharField(
        max_length=255,
        help_text="Valor que representa esta opción para el usuario."
    )

    def get_parent_filter(self):
        if self.field_id:
            return {"field": self.field}
        return {}