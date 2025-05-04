import psycopg2
import traceback

try:
    conn = psycopg2.connect(
        dbname="minitwitter_db",
        user="minitwitter_user",
        password="12345",
        host="localhost",
        port="5432",
        options="-c client_encoding=UTF8"
    )
    print("Conexão bem-sucedida!")
    conn.close()
except Exception:
    print("Erro na conexão:")
    traceback.print_exc()
