import flet as ft

from components.theme import Colors, Spacing, Typography


class PageHeader(ft.Column):
    """Cabeçalho padronizado para páginas da aplicação."""

    def __init__(
        self,
        title: str,
        subtitle: str | None = None,
        show_divider: bool = True,
    ) -> None:
        controls: list[ft.Control] = [
            ft.Text(
                title,
                size=Typography.H1,
                weight=ft.FontWeight.BOLD,
                color=Colors.Text.PRIMARY,
            ),
        ]

        if subtitle:
            controls.append(
                ft.Text(
                    subtitle,
                    size=Typography.BODY,
                    color=Colors.Text.SECONDARY,
                )
            )

        if show_divider:
            controls.append(ft.Divider())

        super().__init__(
            controls=controls,
            spacing=Spacing.SM,
        )