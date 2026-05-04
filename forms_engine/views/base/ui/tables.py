from dataclasses import dataclass
from django.urls import reverse
from django.core.paginator import Paginator

from .styles import StyleBuilderMixin


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
    edit_url: str | None = None
    edit_label: str = "Editar"


class SectionPaginationMixin:
    def paginate_items(self, items, page_param="page", per_page=8):
        paginator = Paginator(items, per_page)
        page_number = self.request.GET.get(page_param)

        return paginator.get_page(page_number)

    def get_sliding_page_range(self, page_obj, window=2):
        current = page_obj.number
        total = page_obj.paginator.num_pages

        start = max(current - window, 1)
        end = min(current + window, total)

        return range(start, end + 1)
    

class DefaultTableSectionMixin(StyleBuilderMixin):
    def build_object_url(self, url_name, obj):
        if not url_name:
            return None

        return reverse(url_name, kwargs={"pk": obj.pk})

    def build_default_table_row(
        self,
        obj,
        detail_url_name=None,
        edit_url_name=None,
    ):
        cells = []

        if hasattr(obj, "order"):
            cells.append(self.build_text_field("Orden", obj.order))

        if hasattr(obj, "label"):
            cells.append(self.build_text_field("Nombre", obj.label))

        if hasattr(obj, "is_active"):
            cells.append(
                self.build_badge_field(
                    "Estado",
                    "Activo" if obj.is_active else "Inactivo",
                    style="success" if obj.is_active else "danger",
                )
            )

        detail_url = self.build_object_url(detail_url_name, obj)
        edit_url = self.build_object_url(edit_url_name, obj)

        return TableRow(
            cells=cells,
            detail_url=detail_url,
            edit_url=edit_url,
        )

    def build_default_table_section(
        self,
        title,
        objects,
        detail_url_name=None,
        edit_url_name=None,
        create_url_name=None,
        create_url_kwargs=None,
        create_label=None,
        empty_message="No hay elementos.",
    ):
        rows = [
            self.build_default_table_row(
                obj,
                detail_url_name=detail_url_name,
                edit_url_name=edit_url_name,
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
            headers=["Orden", "Nombre", "Estado"],
            rows=rows,
            create_url=create_url,
            create_label=create_label,
            empty_message=empty_message,
        )

