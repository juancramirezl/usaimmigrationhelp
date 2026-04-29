from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from .generic import OrderedScopedKeyMixin

"""
Every model should have a is_required attribute?
"""

"""
- Opportunity to add multiple answers to the same question
- Model scenario where 1 question have splitted answers like: entrance (date, place, status)
- Question can come in groups: 
                names-(first, middle, last)
                physical address-(street1, street2, zipcode)
                mailing address-(street1, street2, zipcode)
                travel data-(passport number, expiration date)
                birth data-(date, city, country)
                nationality data-(actual,N at birth)
"""

class FormTemplate(models.Model):
    form_code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Código único de la plantilla dentro de USCIS. Ej: 'I-589'."
    )
    label = models.CharField(
        max_length=255,
        help_text="Texto visible para el usuario. Se mostrará como título o pregunta en la interfaz.",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indica si esta plantilla está activa."
    )

    def __str__(self):
        return f"{self.form_code} - {self.label}"


class FormSection(OrderedScopedKeyMixin):
    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["form_template", "key"],
                name="unique_section_key_per_form",
            ),
            models.UniqueConstraint(
                fields=["form_template", "order"],
                condition=Q(is_active=True),
                name="unique_active_section_order_per_form",
            ),
        ]
        
    form_template = models.ForeignKey(
        FormTemplate,
        on_delete=models.CASCADE,
        related_name="sections",
        help_text="Plantilla a la que pertenece esta sección."
    )
    is_required = models.BooleanField(
        default=False,
        help_text="Indica si esta sección es obligatoria dentro de la plantilla."
    )

    def __str__(self):
        return self.label
    
    def get_parent_filter(self):
        if self.form_template_id:
            return {"form_template": self.form_template}
        return {}
    

class SectionQuestion(OrderedScopedKeyMixin):
    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["section", "key"],
                name="unique_question_key_per_section",
            ),
            models.UniqueConstraint(
                fields=["section", "order"],
                condition=Q(is_active=True),
                name="unique_active_question_order_per_section",
            ),
        ]

    section = models.ForeignKey(
        FormSection,
        on_delete=models.CASCADE,
        related_name="questions",
        help_text="Sección a la que pertenece esta pregunta."
    )
    is_required = models.BooleanField(
        default=False,
        help_text="Indica si esta pregunta es obligatoria."
    )

    def __str__(self):
        return self.label

    def get_parent_filter(self):
        if self.section_id:
            return {"section": self.section}
        return {}
    

class QuestionGroup(OrderedScopedKeyMixin):
    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["question", "key"],
                name="unique_group_key_per_question",
            ),
            models.UniqueConstraint(
                fields=["question", "order"],
                condition=Q(is_active=True),
                name="unique_active_group_order_per_question",
            ),
        ]

    NON_REPEATABLE_ITEM_COUNT = 1

    ERROR_MESSAGES = {
        **OrderedScopedKeyMixin.ERROR_MESSAGES,
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
        SectionQuestion,
        on_delete=models.CASCADE,
        related_name="groups",
        help_text="Pregunta a la que pertenece este grupo."
    )
    is_repeatable = models.BooleanField(
        default=False,
        help_text="Indica si este grupo puede repetirse múltiples veces."
    )
    min_items = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Cantidad mínima de veces que se puede completar este grupo (todos sus campos)."
    )

    max_items = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        help_text="Cantidad máxima de veces que se puede completar este grupo (todos sus campos). Puede dejarse vacío si no hay límite."
)
    is_required = models.BooleanField(
        default=False,
        help_text="Indica si este grupo es obligatorio."
    )

    def __str__(self):
        return self.label

    def get_parent_filter(self):
        if self.question_id:
            return {"question": self.question}
        return {}

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
            errors["min_items"] = self.ERROR_MESSAGES["non_repeatable_min_items"]

        if self.max_items != self.NON_REPEATABLE_ITEM_COUNT:
            errors["max_items"] = self.ERROR_MESSAGES["non_repeatable_max_items"]

        return errors

    def _get_repeatable_group_errors(self):
        errors = {}

        if self.max_items == self.NON_REPEATABLE_ITEM_COUNT:
            errors["max_items"] = self.ERROR_MESSAGES["repeatable_max_items_one"]

        if self._max_items_is_less_than_min_items():
            errors["max_items"] = self.ERROR_MESSAGES["max_items_less_than_min_items"]

        return errors

    def _max_items_is_less_than_min_items(self):
        return self.max_items is not None and self.max_items < self.min_items
    

class GroupField(OrderedScopedKeyMixin):
    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["group", "key"],
                name="unique_field_key_per_group",
            ),
            models.UniqueConstraint(
                fields=["group", "order"],
                condition=Q(is_active=True),
                name="unique_active_field_order_per_group",
            ),
        ]

    ERROR_MESSAGES = {
        **OrderedScopedKeyMixin.ERROR_MESSAGES,
        "select_requires_option_source": _(
            "Los campos tipo select deben definir una fuente de opciones."
        ),
        "only_select_uses_option_source": _(
            "Solo los campos tipo select pueden definir una fuente de opciones."
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
    is_required = models.BooleanField(
        default=False,
        help_text="Indica si este campo es obligatorio."
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
            errors["option_source"] = self.ERROR_MESSAGES[
                "select_requires_option_source"
            ]

        if not self.is_select_field and self.has_option_source:
            errors["option_source"] = self.ERROR_MESSAGES[
                "only_select_uses_option_source"
            ]

        return errors
    
    def _get_locked_option_config_errors(self):
        errors = {}

        if not self.pk:
            return errors

        old = type(self).objects.get(pk=self.pk)

        has_existing_options = old.options.exists()

        if not has_existing_options:
            return errors

        if old.field_type != self.field_type:
            errors["field_type"] = _(
                "No puedes cambiar el tipo de campo porque ya existen opciones asociadas."
            )

        if old.option_source != self.option_source:
            errors["option_source"] = _(
                "No puedes cambiar la fuente de opciones porque ya existen opciones asociadas."
            )

        return errors


class FieldOption(OrderedScopedKeyMixin):
    class Meta:
        ordering = ["order"]
        constraints = [
            models.UniqueConstraint(
                fields=["field", "key"],
                name="unique_option_key_per_field",
            ),
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

    def __str__(self):
        return self.label

    def get_parent_filter(self):
        if self.field_id:
            return {"field": self.field}
        return {}