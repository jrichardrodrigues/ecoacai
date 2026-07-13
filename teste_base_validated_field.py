import flet as ft

from components.fields import BaseValidatedField


class CampoTeste(BaseValidatedField):

    def validar(self):
        texto = self.value.strip()

        if not texto:
            self.limpar_mensagem()
            return

        if len(texto) < 5:
            self.erro("Digite pelo menos 5 caracteres.")
            return

        self.sucesso("Campo válido.")


def main(page: ft.Page):
    page.title = "Teste BaseValidatedField"

    campo = CampoTeste(
        label="Digite qualquer texto",
        hint_text="Mínimo de 5 caracteres",
    )

    page.add(
        ft.Column(
            controls=[
                ft.Text(
                    "Teste de validação automática",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                campo.container,
            ],
            spacing=20,
        )
    )


if __name__ == "__main__":
    ft.run(main=main)