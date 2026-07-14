from services import EmailService

from .base_validated_field import BaseValidatedField


class EmailField(BaseValidatedField):

    def __init__(
        self,
        usuario_service=None,
        ignorar_id: int = 0,
    ):
        super().__init__(
            label="E-mail",
            hint_text="exemplo@email.com",
        )

        self.usuario_service = usuario_service
        self.ignorar_id = ignorar_id

    def validar(self):
        email = EmailService.normalizar(self.value)

        if email != self.control.value:
            self.control.value = email

        if not email:
            self.limpar_mensagem()
            return

        valido, mensagem = EmailService.validar(email)

        if not valido:
            self.erro(mensagem)
            return

        if (
            self.usuario_service is not None
            and self.usuario_service.email_existe(
                email,
                ignorar_id=self.ignorar_id,
            )
        ):
            self.erro("E-mail já cadastrado.")
            return

        self.sucesso("E-mail com formato válido.")