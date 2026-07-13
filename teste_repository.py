from repositories import JsonRepository

repo = JsonRepository()

dados = repo.carregar()

print(dados)