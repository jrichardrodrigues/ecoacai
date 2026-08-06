import flet as ft

from components.theme import Colors, Spacing


class ZPage(ft.Container):
    """
    Container base de todas as telas da plataforma ZELURBIS.
    """

    def __init__(
        self,
        content: ft.Control,
        *,
        padding: int | None = None,
        max_width: int = 1400,
        alignment=ft.Alignment.TOP_CENTER,
    ):
        super().__init__()

        self.expand = True
        self.bgcolor = Colors.BACKGROUND

        self.alignment = alignment

        self.padding = (
            padding
            if padding is not None
            else Spacing.PAGE_PADDING
        )

        self.content = ft.SafeArea(
            expand=True,
            content=ft.Container(
                expand=True,
                alignment=ft.alignment.top_center,
                content=ft.Container(
                    width=max_width,
                    expand=True,
                    content=content,
                ),
            ),
        )