import flet as ft


class HomeView:
    """Conteúdo da página inicial do ECOAÇAÍ."""

    def build(self) -> ft.Control:
        marca_dagua = ft.Container(
            expand=True,
            alignment=ft.Alignment(0.88, 0.28),
            content=ft.Image(
                src="assets/svg/ecoacai_watermark.svg",
                width=430,
                height=430,
                fit=ft.BoxFit.CONTAIN,
            ),
        )

        conteudo_principal = ft.Container(
            expand=True,
            padding=40,
            content=ft.Column(
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Text(
                        "Bem-vindo ao ECOAÇAÍ",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Container(
                        width=90,
                        height=4,
                        border_radius=10,
                        bgcolor=ft.Colors.PINK_800,
                    ),
                    ft.Text(
                        "Gerencie estabelecimentos, coletas, "
                        "indicadores e operações ambientais "
                        "em uma única plataforma.",
                        size=17,
                        color=ft.Colors.GREY_800,
                    ),
                    ft.Row(
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(
                                ft.Icons.INFO_OUTLINE,
                                color=ft.Colors.PINK_800,
                            ),
                            ft.Text(
                                "Utilize o menu lateral para acessar "
                                "os módulos do sistema.",
                                size=16,
                                color=ft.Colors.GREY_800,
                            ),
                        ],
                    ),
                ],
            ),
        )

        return ft.Stack(
            expand=True,
            controls=[
                marca_dagua,
                conteudo_principal,
            ],
        )