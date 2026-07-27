from repositories.veiculo_repository import VeiculoRepository
from models import Veiculo


def main():
    repo = VeiculoRepository()

    print("=" * 60)
    print("TESTE DO REPOSITÓRIO DE VEÍCULOS")
    print("=" * 60)

    veiculo = Veiculo(
        placa="QWE1A23",
        marca="Mercedes",
        modelo="Atego 1719",
        ano=2023,
        tipo="Caminhão",
        capacidade=12000,
        motorista_id=None,
    )

    try:
        veiculo = repo.cadastrar(veiculo)
        print("✔ Veículo cadastrado")
        print(veiculo)

    except Exception as erro:
        print("Erro:", erro)
        return

    print("\nBuscando por placa...")

    encontrado = repo.buscar_por_placa("QWE1A23")

    if encontrado:
        print("✔ Encontrado")
        print(encontrado)
    else:
        print("Não encontrado")


if __name__ == "__main__":
    main()