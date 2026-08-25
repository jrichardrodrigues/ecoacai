import flet as ft


class DataTable(ft.DataTable):
    """Tabela padrão utilizada pelo sistema."""

    def __init__(
        self,
        columns: list[ft.DataColumn],
    ) -> None:
        super().__init__(
            columns=columns,
            rows=[],
            border=ft.Border.all(
                width=1,
                color=ft.Colors.GREY_300,
            ),
            border_radius=10,
            column_spacing=40,
            horizontal_lines=ft.BorderSide(
                width=1,
                color=ft.Colors.GREY_200,
            ),
            heading_row_height=52,
            data_row_min_height=48,
            data_row_max_height=56,
            expand=True,
        )

    def atualizar(
        self,
        rows: list[ft.DataRow],
    ) -> None:
        self.rows = rows