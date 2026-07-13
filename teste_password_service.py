from services import PasswordService


service = PasswordService()

senhas_teste = [
    "",
    "carlos",
    "Carlos123",
    "@carlos12",
    "@CARLOS12",
    "@Carlos12",
]

for senha in senhas_teste:
    sucesso, mensagem = service.validar_regra(senha)

    print(
        f"Senha: {senha!r} "
        f"| Válida: {sucesso} "
        f"| Mensagem: {mensagem}"
    )

senha_valida = "@Carlos12"

hash_gerado = service.gerar_hash(senha_valida)

print("\nHash gerado:")
print(hash_gerado)

print(
    "\nSenha correta:",
    service.verificar(
        senha_valida,
        hash_gerado,
    ),
)

print(
    "Senha incorreta:",
    service.verificar(
        "@Carlos99",
        hash_gerado,
    ),
)

print(
    "Confirmação correta:",
    service.validar_confirmacao(
        senha_valida,
        "@Carlos12",
    ),
)

print(
    "Confirmação incorreta:",
    service.validar_confirmacao(
        senha_valida,
        "@Carlos13",
    ),
)

print(
    "Precisa rehash:",
    service.precisa_rehash(hash_gerado),
)