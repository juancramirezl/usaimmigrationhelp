from django.db import models


class FormTemplate(models.Model):
    code = models.CharField(max_length=50, unique=True) #I-589
    name = models.CharField(max_length=255) #Asylum and Withoulding of Removal
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class FormSection(models.Model):
    form_template = models.ForeignKey(
        FormTemplate,
        on_delete=models.CASCADE,
        related_name="sections",
    )
    title = models.CharField(max_length=255) #User Display Name
    key = models.CharField(max_length=100) #Internal key biography, personal_data
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]
        unique_together = ("form_template", "key")

    def __str__(self):
        return self.title


class Question(models.Model):
    FIELD_TYPES = [
        ("text", "Text"),
        ("textarea", "Textarea"),
        ("date", "Date"),
        ("select", "Select"),
        ("radio", "Radio"),
        ("boolean", "Boolean"),
    ]

    OPTION_SOURCES = [
        ("none", "None"),
        ("db", "Database"),
        ("countries", "Countries Library"),
        ("us_states", "US States Catalog"),
    ]

    section = models.ForeignKey(
        "forms_engine.FormSection",
        on_delete=models.CASCADE,
        related_name="questions",
    )
    key = models.CharField(max_length=100)
    label = models.CharField(max_length=255)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    option_source = models.CharField(
        max_length=20,
        choices=OPTION_SOURCES,
        default="none",
    )
    required = models.BooleanField(default=False)
    order = models.PositiveIntegerField()


class QuestionOption(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="options",
    )
    value = models.CharField(max_length=100) #Internal yes, no
    label = models.CharField(max_length=255) #User Display Sí, No
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.label
