from .confirm_dialog import ConfirmDialog


def confirmar_exclusao(
    page,
    mensagem,
    on_confirm,
):
    """Compatibilidade com o código antigo."""

    dialog = ConfirmDialog(
        page=page,
        titulo="Confirmar exclusão",
        mensagem=mensagem,
        on_confirm=on_confirm,
    )

    page.overlay.append(dialog)
    dialog.open = True
    page.update()

    return dialog


__all__ = [
    "ConfirmDialog",
    "confirmar_exclusao",
]