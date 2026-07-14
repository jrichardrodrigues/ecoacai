import flet as ft


class ActionButtons(ft.Row):
    """Botões de ação utilizados nas tabelas."""

    def __init__(
        self,
        on_edit=None,
        on_delete=None,
        on_collect=None,
    ):
        super().__init__(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.EDIT_OUTLINED,
                    tooltip="Editar",
                    icon_color=ft.Colors.BLUE,
                    on_click=on_edit,
                ),
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    tooltip="Excluir",
                    icon_color=ft.Colors.RED,
                    on_click=on_delete,
                ),
                ft.IconButton(
                    icon=ft.Icons.LOCAL_SHIPPING_OUTLINED,
                    tooltip="Solicitar coleta",
                    icon_color=ft.Colors.GREEN,
                    on_click=on_collect,
                ),
            ],
            spacing=0,
        )