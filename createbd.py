import sqlite3

def create_db():
    conn = sqlite3.connect('./BD/config.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS email_config (
            id INTEGER PRIMARY KEY,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            smtp_server TEXT NOT NULL,
            smtp_port INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Chamar a função para criar a tabela
create_db()
