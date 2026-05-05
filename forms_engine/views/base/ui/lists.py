from dataclasses import dataclass
from django.core.paginator import Paginator


@dataclass
class ListItem:
    title: str
    subtitle: object | None = None


@dataclass
class ListSection:
    title: str
    items: list[ListItem]
    empty_message: str = "No hay elementos."
    page_obj: object | None = None
    page_param: str | None = None
    page_range: object | None = None
    type: str = "list"
    

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


class DefaultListSectionMixin(SectionPaginationMixin):
    def build_default_list_section(
        self,
        title,
        choices,
        page_param,
        empty_message="No hay elementos.",
        per_page=8,
    ):
        items = [
            ListItem(
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

        return ListSection(
            title=title,
            items=page_obj.object_list,
            empty_message=empty_message,
            page_obj=page_obj,
            page_param=page_param,
            page_range=self.get_sliding_page_range(page_obj),
        )