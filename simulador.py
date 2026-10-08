import sqlite3
import time
import random
from datetime import datetime


def init_db():

    conn = sqlite3.connect("Servidores.db", timeout=10)
    cursor = conn.cursor()

    cursor.execute("PRAGMA journal_mode=WAL;")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leituras_servidores(

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            servidor_id TEXT,
            uso_cpu REAL,
            uso_memoria REAL,
            latencia REAL,
            temperatura_cpu REAL

        )
    ''')

    conn.commit()
    conn.close()


def simulador_servidores():

    init_db()

    print("Simulador de servidores em execução...")

    # Valores base dos servidores
    servidores = {

        'Servidor A': {
            'cpu': 45.0,
            'memoria': 58.0,
            'latencia': 12.0,
            'temperatura': 48.0
        },

        'Servidor B': {
            'cpu': 62.0,
            'memoria': 70.0,
            'latencia': 18.0,
            'temperatura': 55.0
        },

        'Servidor C': {
            'cpu': 35.0,
            'memoria': 45.0,
            'latencia': 9.0,
            'temperatura': 42.0
        }

    }

    while True:

        try:

            conn = sqlite3.connect("Servidores.db", timeout=10)
            cursor = conn.cursor()

            for servidor_id, dados in servidores.items():

                # Simular variações nos valores dos servidores
                cpu = round(
                    max(0, min(100, dados['cpu'] + random.uniform(-4, 4))),
                    2
                )

                memoria = round(
                    max(0, min(100, dados['memoria'] + random.uniform(-3, 3))),
                    2
                )

                latencia = round(
                    max(1, dados['latencia'] + random.uniform(-2, 2)),
                    2
                )

                temperatura = round(
                    max(0, dados['temperatura'] + random.uniform(-1.5, 1.5)),
                    2
                )

                # Atualiza referência para variação fluida
                dados['cpu'] = cpu
                dados['memoria'] = memoria
                dados['latencia'] = latencia
                dados['temperatura'] = temperatura

                timestamp = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                cursor.execute('''
                    INSERT INTO leituras_servidores
                    (
                        timestamp,
                        servidor_id,
                        uso_cpu,
                        uso_memoria,
                        latencia,
                        temperatura_cpu
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    timestamp,
                    servidor_id,
                    cpu,
                    memoria,
                    latencia,
                    temperatura
                ))

            conn.commit()
            conn.close()

            print(
                f"[{datetime.now().strftime('%H:%M:%S')}] "
                "Novas leituras dos servidores inseridas."
            )

            time.sleep(2)  # Aguarda 2 segundos antes da próxima leitura

        except sqlite3.OperationalError as e:

            print(f"Aviso de ocorrência: {e}.")
            time.sleep(1)

        except KeyboardInterrupt:

            print("\nSimulação finalizada.")
            break


if __name__ == "__main__":
    simulador_servidores()