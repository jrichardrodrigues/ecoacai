from models.motorista import Motorista


motorista = Motorista(
    nome="João da Silva",
    telefone="(91) 99999-9999",
    cnh="12345678900",
    categoria_cnh="D",
)

print(motorista)
print(motorista.to_dict())

motorista_recuperado = Motorista.from_dict(
    {
        "id": 1,
        "nome": "Carlos Souza",
        "telefone": "(91) 98888-7777",
        "cnh": "98765432100",
        "categoria_cnh": "C",
        "ativo": 1,
    }
)

print(motorista_recuperado)