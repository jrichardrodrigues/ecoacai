from services import CpfService

from .base_validated_field import BaseValidatedField


class CpfField(BaseValidatedField):

    def __init__(
        self,
        usuario_service,
        ignorar_id: int = 0,
    ):
        super().__init__(
            label="CPF",
            max_length=14,
        )

        self.usuario_service = usuario_service
        self.ignorar_id = ignorar_id

    def validar(self):
        cpf = CpfService.formatar(self.value)

        if cpf != self.control.value:
            self.control.value = cpf

        if not cpf:
            self.limpar_mensagem()
            return

        if len(CpfService.remover_formatacao(cpf)) < 11:
            self.erro("Digite os 11 números do CPF.")
            return

        if not CpfService.validar(cpf):
            self.erro("CPF inválido.")
            return

        if self.usuario_service.cpf_existe(
            cpf,
            ignorar_id=self.ignorar_id,
        ):
            self.erro("CPF já cadastrado.")
            return

        self.sucesso("CPF válido.")