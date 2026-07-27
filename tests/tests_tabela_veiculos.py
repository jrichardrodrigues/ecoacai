# from repositories.sqlite_database import SQLiteDatabase
#
# SQLiteDatabase().inicializar()
#
# print("Banco atualizado com sucesso!")

##################################################################

# from repositories.sqlite_database import SQLiteDatabase
#
# db = SQLiteDatabase()
#
# with db.obter_conexao() as conexao:
#     print("=== COLUNAS DA TABELA VEICULOS ===")
#
#     cursor = conexao.execute(
#         "PRAGMA table_info(veiculos)"
#     )
#
#     for coluna in cursor.fetchall():
#         print(dict(coluna))

##################################################################

from repositories.sqlite_database import SQLiteDatabase

db = SQLiteDatabase()

with db.obter_conexao() as conexao:
    print("\n=== ÍNDICES DA TABELA VEICULOS ===\n")

    cursor = conexao.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'index'
          AND tbl_name = 'veiculos'
        ORDER BY name
    """)

    indices = cursor.fetchall()

    if not indices:
        print("Nenhum índice encontrado.")
    else:
        for indice in indices:
            print(indice["name"])
