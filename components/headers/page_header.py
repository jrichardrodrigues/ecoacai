import flet as ft

from components.theme import Colors, Spacing, Typography


class PageHeader(ft.Column):
    """Cabeçalho padrão das telas do EcoAçaí."""

    def __init__(
        self,
        title: str,
        subtitle: str = "",
        icon=ft.Icons.ECO,
    ):
        super().__init__()

        self.spacing = Spacing.SM
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        controls = [
            ft.Icon(
                icon,
                size=52,
                color=Colors.PRIMARY,
            ),

            ft.Text(
                title,
                size=Typography.TITLE,
                weight=ft.FontWeight.BOLD,
                color=Colors.PRIMARY,
            ),
        ]

        if subtitle:
            controls.append(
                ft.Text(
                    subtitle,
                    size=Typography.BODY,
                    color=Colors.TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER,
                )
            )

        self.controls = controls