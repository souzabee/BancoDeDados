# -*- coding: utf-8 -*-

# pip install psycopg2-binary


# CRIAÇÃO DE TABELA E INSERÇÃO DE DADOS NO POSTGRESQL
import psycopg2

from exmeplo_segredos import BD_NOME, BD_USUARIO, BD_SENHA, BD_HOST, BD_PORTA

try:
    conn = psycopg2.connect(database=BD_NOME,
                            user=BD_USUARIO,
                            password=BD_SENHA,
                            host=BD_HOST,
                            port=BD_PORTA)
    print("Banco de dados conectado com sucesso")

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS empregado
    (
        ID INT PRIMARY KEY NOT NULL,
        NOME TEXT NOT NULL,
        EMAIL TEXT NOT NULL
    )
    """)

    conn.commit()
    print("Tabela criada com sucesso (ou já existia)")
    cur.close()

except Exception as e:
    print(f"Falha na conexão ou criação da tabela: {e}")
finally:
    if 'conn' in locals() and conn is not None:
        conn.close()
        print("Conexão inicial fechada.")


# INSERÇÃO DE DADOS NO POSTGRESQL
try:
    conn = psycopg2.connect(database=BD_NOME,
                            user=BD_USUARIO,
                            password=BD_SENHA,
                            host=BD_HOST,
                            port=BD_PORTA)
    print("Banco de dados conectado para inserção.")

    cur = conn.cursor()

    sql_insert = "INSERT INTO empregado (ID, NOME, EMAIL) VALUES (%s, %s, %s) ON CONFLICT (ID) DO NOTHING" # Evita erro se ID já existir
    dados = [
        (1, 'Ada Lovelace', 'ada@lovelace.com'),
        (2, 'Radia Perlman', 'Radia@Perlman.com')
    ]
    cur.executemany(sql_insert, dados)

    conn.commit()
    print(f"Dados inseridos com sucesso (ou ignorados se já existiam). Linhas afetadas: {cur.rowcount}")

    cur.close()

except Exception as e:
    print(f"Falha ao inserir dados: {e}")
finally:
    if 'conn' in locals() and conn is not None:
        conn.close()
        print("Conexão de inserção fechada.")


# RECUPERAÇÃO DE DADOS DO POSTGRESQL
try:
    conn = psycopg2.connect(database=BD_NOME,
                            user=BD_USUARIO,
                            password=BD_SENHA,
                            host=BD_HOST,
                            port=BD_PORTA)
    print("Banco de dados conectado para busca.")

    cur = conn.cursor()

    cur.execute("SELECT ID, NOME, EMAIL FROM empregado")
    rows = cur.fetchall()

    print("\n--- Dados Atuais na Tabela ---")
    if rows:
        for data in rows:
            print(f"ID    : {data[0]}")
            print(f"NOME  : {data[1]}")
            print(f"EMAIL : {data[2]}")
            print("-----------------------------")
        print('Dados buscados com sucesso')
    else:
        print("Nenhum dado encontrado na tabela.")

    cur.close()

except Exception as e:
    print(f"Falha ao buscar dados: {e}")
finally:
    if 'conn' in locals() and conn is not None:
        conn.close()
        print("Conexão de busca fechada.")


# ATUALIZAÇÃO DE DADOS NO POSTGRESQL
try:
    conn = psycopg2.connect(database=BD_NOME, user=BD_USUARIO, password=BD_SENHA,
                            host=BD_HOST, port=BD_PORTA)
    print("Banco de dados conectado para atualização.")

    cur = conn.cursor()

    sql_update = "UPDATE empregado SET EMAIL = %s WHERE ID = %s"
    novo_email = 'atualizado@gmail.com'
    id_para_atualizar = 1
    cur.execute(sql_update, (novo_email, id_para_atualizar))

    conn.commit()
    print("Dados atualizados com sucesso")
    print(f"Total de linhas afetadas: {cur.rowcount}")

    cur.close()

except Exception as e:
    print(f"Falha ao atualizar dados: {e}")
finally:
    if 'conn' in locals() and conn is not None:
        conn.close()
        print("Conexão de atualização fechada.")

# REMOÇÃO DE DADOS NO POSTGRESQL
try:
    conn = psycopg2.connect(database=BD_NOME, user=BD_USUARIO, password=BD_SENHA,
                            host=BD_HOST, port=BD_PORTA)
    print("Banco de dados conectado para exclusão.")

    cur = conn.cursor()

    sql_delete = "DELETE FROM empregado WHERE ID = %s"
    id_para_excluir = 1
    cur.execute(sql_delete, (id_para_excluir,))

    conn.commit()
    print("Dados excluídos com sucesso")
    print(f"Total de linhas afetadas: {cur.rowcount}")

    cur.close()

except Exception as e:
    print(f"Falha ao excluir dados: {e}")
finally:
    if 'conn' in locals() and conn is not None:
        conn.close()
        print("Conexão de exclusão fechada.")

print("\nScript finalizado.")
