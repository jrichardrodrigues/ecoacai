from repositories.sqlite_database import SQLiteDatabase

database = SQLiteDatabase()
database.inicializar()

print("Banco inicializado com sucesso.")

with database.obter_conexao() as conexao:
    colunas = conexao.execute(
        "PRAGMA table_info(motoristas)"
    ).fetchall()

    for coluna in colunas:
        print(dict(coluna))