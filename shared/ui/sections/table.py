from dataclasses import dataclass
from django.urls import reverse

from ..styling.fields import UIFieldBuilderMixin


@dataclass
class TableField:
    label: str
    attr: str
    field_type: str = "text"


@dataclass
class TableSection:
    title: str
    headers: list[str]
    rows: list
    create_url: str | None = None
    create_label: str | None = None
    empty_message: str = "No hay elementos."
    type: str = "table"


@dataclass
class TableRow:
    cells: list
    detail_url: str | None = None
    detail_label: str = "Ver"
    update_url: str | None = None
    update_label: str = "Editar"


class TableSectionMixin(UIFieldBuilderMixin):
    table_fields = ()

    def get_table_fields(self):
        return self.table_fields

    def get_resolved_table_fields(self, objects):
        objects = list(objects)

        if not objects:
            return self.get_table_fields()

        sample_obj = objects[0]

        return [
            field
            for field in self.get_table_fields()
            if hasattr(sample_obj, field.attr)
        ]

    def build_object_url(self, url_name, obj):
        if not url_name:
            return None

        return reverse(url_name, kwargs={"pk": obj.pk})

    def build_table_cell(self, obj, field):
        value = getattr(obj, field.attr, None)

        if field.field_type == "status":
            return self.build_badge_field(
                field.label,
                "Activo" if value else "Inactivo",
                style="success" if value else "danger",
            )

        if field.field_type == "boolean":
            return self.build_badge_field(
                field.label,
                "Sí" if value else "No",
                style="success" if value else "secondary",
            )

        return self.build_text_field(field.label, value)

    def build_default_table_row(
        self,
        obj,
        fields,
        detail_url_name=None,
        update_url_name=None,
    ):
        cells = [
            self.build_table_cell(
                obj=obj,
                field=field,
            )
            for field in fields
        ]

        return TableRow(
            cells=cells,
            detail_url=self.build_object_url(detail_url_name, obj),
            update_url=self.build_object_url(update_url_name, obj),
        )

    def build_default_table_section(
        self,
        title,
        objects,
        detail_url_name=None,
        update_url_name=None,
        create_url_name=None,
        create_url_kwargs=None,
        create_label=None,
        empty_message="No hay elementos.",
    ):
        objects = list(objects)
        fields = self.get_resolved_table_fields(objects)

        rows = [
            self.build_default_table_row(
                obj=obj,
                fields=fields,
                detail_url_name=detail_url_name,
                update_url_name=update_url_name,
            )
            for obj in objects
        ]

        create_url = (
            reverse(create_url_name, kwargs=create_url_kwargs or {})
            if create_url_name
            else None
        )

        return TableSection(
            title=title,
            headers=[
                field.label
                for field in fields
            ],
            rows=rows,
            create_url=create_url,
            create_label=create_label,
            empty_message=empty_message,
        )