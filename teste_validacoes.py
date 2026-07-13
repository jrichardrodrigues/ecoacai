from services import CpfService
from utils.validators import email_valido, campo_obrigatorio, numero_inteiro_positivo


print("CPF válido:", CpfService.validar("529.982.247-25"))
print("CPF inválido:", CpfService.validar("111.111.111-11"))
print("CPF formatado:", CpfService.formatar("52998224725"))

print("E-mail válido:", email_valido("cliente@email.com"))
print("E-mail inválido:", email_valido("cliente@email"))

print("Campo obrigatório:", campo_obrigatorio("Maria"))
print("Campo vazio:", campo_obrigatorio(""))

print("Número positivo:", numero_inteiro_positivo("3"))
print("Número inválido:", numero_inteiro_positivo("abc"))