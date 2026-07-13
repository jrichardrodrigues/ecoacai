from repositories import SQLiteDatabase


database = SQLiteDatabase()

database.inicializar()

print("Banco SQLite inicializado com sucesso.")
print("Arquivo:", database.database_path)

with database.obter_conexao() as conexao:
    tabelas = conexao.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
        """
    ).fetchall()

    print("\nTabelas encontradas:")

    for tabela in tabelas:
        print("-", tabela["name"])