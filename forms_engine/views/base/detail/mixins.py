from django.urls import reverse
from django.core.paginator import Paginator


class StyleBuilderMixin:
    DEFAULT_BADGE_STYLE = "secondary"

    BADGE_STYLES = {
        "success": "bg-success",
        "danger": "bg-danger",
        "warning": "bg-warning",
        "info": "bg-info",
        "primary": "bg-primary",
        "secondary": "bg-secondary",
        "dark": "bg-dark",
    }

    def build_badge(self, label, value, style=None):
        style = style or self.DEFAULT_BADGE_STYLE

        return {
            "label": label,
            "value": value,
            "badge_class": self.BADGE_STYLES.get(
                style,
                self.BADGE_STYLES[self.DEFAULT_BADGE_STYLE],
            ),
        }
    
    """
    Replace Flag of is_badge with type (text, badge)
    """
    def build_text_field(self, label, value):
        return {
            "label": label,
            "value": value,
            "is_badge": False,
        }

    def build_badge_field(self, label, value, style=None):
        badge_item = self.build_badge(
            label=label,
            value=value,
            style=style
        )
        badge_item["is_badge"] = True

        return badge_item
    

class TableBuilderMixin:
    def build_table_section(
        self,
        title,
        headers,
        rows,
        create_url=None,
        create_label=None,
        empty_message="No hay elementos.",
    ):
        return {
            "type": "table",
            "title": title,
            "headers": headers,
            "rows": rows,
            "create_url": create_url,
            "create_label": create_label,
            "empty_message": empty_message,
        }

    def build_table_row(self, cells, detail_url=None, detail_label="Ver"):
        return {
            "cells": cells,
            "detail_url": detail_url,
            "detail_label": detail_label,
        }


class AccordionBuilderMixin:
    def build_accordion_item(
        self,
        order,
        title,
        subtitle=None,
        fields=None,
        detail_url=None,
        detail_label="Ver",
    ):
        return {
            "order": order,
            "title": title,
            "subtitle": subtitle,
            "fields": fields or [],
            "detail_url": detail_url,
            "detail_label": detail_label,
        }

    def build_accordion_section(
        self,
        title,
        items,
        accordion_id,
        create_url=None,
        create_label=None,
        empty_message="No hay elementos.",
    ):
        return {
            "type": "accordion",
            "title": title,
            "items": items,
            "accordion_id": accordion_id,
            "create_url": create_url,
            "create_label": create_label,
            "empty_message": empty_message,
        }
    
    
class ListBuilderMixin:
    def build_list_item(self, title, subtitle=None):
        return {
            "title": title,
            "subtitle": subtitle,
        }

    def build_list_section(
        self,
        title,
        items,
        empty_message="No hay elementos.",
    ):
        return {
            "type": "list",
            "title": title,
            "items": items,
            "empty_message": empty_message,
        }
    

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
    

class DefaultTableSectionMixin(
    TableBuilderMixin,
    StyleBuilderMixin,
):
    def build_default_table_row(self, obj, detail_url_name=None):
        cells = []

        if hasattr(obj, "order"):
            cells.append(self.build_text_field("Orden", obj.order))

        if hasattr(obj, "label"):
            cells.append(self.build_text_field("Nombre", obj.label))

        if hasattr(obj, "key"):
            cells.append(self.build_text_field("Key", obj.key))

        if hasattr(obj, "is_active"):
            cells.append(
                self.build_badge_field(
                    "Estado",
                    "Activo" if obj.is_active else "Inactivo",
                    style="success" if obj.is_active else "danger",
                )
            )

        detail_url = None

        if detail_url_name:
            detail_url = reverse(detail_url_name, kwargs={"pk": obj.pk})

        return self.build_table_row(
            cells=cells,
            detail_url=detail_url,
        )

    def build_default_table_section(
        self,
        title,
        objects,
        detail_url_name=None,
        create_url_name=None,
        create_url_kwargs=None,
        create_label=None,
        empty_message="No hay elementos.",
    ):
        rows = [
            self.build_default_table_row(obj, detail_url_name)
            for obj in objects
        ]

        create_url = None

        if create_url_name:
            create_url = reverse(
                create_url_name,
                kwargs=create_url_kwargs or {},
            )

        return self.build_table_section(
            title=title,
            headers=["Orden", "Nombre", "Key", "Estado"],
            rows=rows,
            create_url=create_url,
            create_label=create_label,
            empty_message=empty_message,
        )
    

class DefaultAccordionSectionMixin(
    AccordionBuilderMixin,
    StyleBuilderMixin
):
    def build_default_object_fields(self, obj):
        fields = []

        if hasattr(obj, "label"):
            fields.append(
                self.build_text_field("Nombre", obj.label)
            )

        if hasattr(obj, "key"):
            fields.append(
                self.build_text_field("Key", obj.key)
            )

        if hasattr(obj, "order"):
            fields.append(
                self.build_text_field("Orden", obj.order)
            )

        return fields

    def build_object_detail_url(self, obj, url_name=None):
        if not url_name:
            return None

        return reverse(url_name, kwargs={"pk": obj.pk})

    def build_default_accordion_item(self, obj, detail_url_name=None):
        title = getattr(obj, "label", str(obj))

        order = None
        if hasattr(obj, "order"):
            order = obj.order

        subtitle = None
        if hasattr(obj, "is_active"):
            subtitle = (
                self.build_badge_field(
                    "Estado",
                    "Activo" if obj.is_active else "Inactivo",
                    style="success" if obj.is_active else "danger",
                )
            )

        return self.build_accordion_item(
            order=order,
            title=title,
            subtitle=subtitle,
            fields=self.build_default_object_fields(obj),
            detail_url=self.build_object_detail_url(obj, detail_url_name),
        )

    def build_default_accordion_section(
        self,
        title,
        objects,
        accordion_id,
        detail_url_name=None,
        create_url_name=None,
        create_url_kwargs=None,
        create_label=None,
        empty_message="No hay elementos.",
    ):
        items = [
            self.build_default_accordion_item(obj, detail_url_name)
            for obj in objects
        ]

        create_url = None

        if create_url_name:
            create_url = reverse(
                create_url_name,
                kwargs=create_url_kwargs or {},
            )

        return self.build_accordion_section(
            title=title,
            items=items,
            accordion_id=accordion_id,
            create_url=create_url,
            create_label=create_label,
            empty_message=empty_message,
        )


class DefaultListSectionMixin(
    ListBuilderMixin,
    SectionPaginationMixin,
):
    def build_default_list_section(
        self,
        title,
        choices,
        page_param,
        empty_message="No hay elementos.",
        per_page=8,
    ):
        items = [
            self.build_list_item(
                title=name,
                subtitle=code,
            )
            for code, name in choices
        ]

        page_obj = self.paginate_items(
            items,
            page_param=page_param,
            per_page=per_page,
        )

        section = self.build_list_section(
            title=title,
            items=page_obj.object_list,
            empty_message=empty_message,
        )

        section["page_obj"] = page_obj
        section["page_param"] = page_param
        section["page_range"] = self.get_sliding_page_range(page_obj)

        return section