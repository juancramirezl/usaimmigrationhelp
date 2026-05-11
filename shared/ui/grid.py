from dataclasses import dataclass


@dataclass
class Grid:
    title: str
    description: str | None
    items: list
    columns: int = 3
    type: str = "grid"

    MIN_COLUMNS = 1
    MAX_COLUMNS = 3

    @property
    def resolved_columns(self):
        return min(max(self.columns, self.MIN_COLUMNS), self.MAX_COLUMNS)

    @property
    def rows(self):
        columns = self.resolved_columns

        return [
            self.items[index:index + columns]
            for index in range(0, len(self.items), columns)
        ]

    @property
    def column_class(self):
        column_size = 12 // self.resolved_columns
        return f"col-12 col-md-{column_size}"