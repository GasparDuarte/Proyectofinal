
import requests
import json
import psycopg2
from datetime import datetime
import pandas as pd
import os
from dotenv import load_dotenv
import sys

# Función para obtener los datos del top 10 de criptos
def get_top_10_crypto_data():
    url = f"{base_url}tickers"
    params = {
        "quotes": "USD",
        "limit": 10
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error al obtener los datos del top 10 de criptos. Código de estado: {response.status_code}")
        print(f"Contenido de la respuesta: {response.text}")
        sys.exit(1)

# Función para cargar los datos en la base de datos
def cargar_datos(crypto_df, conn):
    try:
        # Obtener el cursor
        cursor = conn.cursor()

        # Cargar los datos en la tabla crypto_data
        for index, row in crypto_df.iterrows():
            coin_name = row['name']
            symbol = row['symbol']
            price = row['quotes']['USD']['price']
            price_change = row['quotes']['USD']['percent_change_24h']
            # Calcular el price_movement
            if price_change > 0:
                price_movement = 'up'
            elif price_change < 0:
                price_movement = 'down'
            else:
                price_movement = 'stable'
            data_extraction_time = datetime.now()

            # Verificar si las cryptos ya están en la tabla para la fecha y hora actual
            select_query = """
                SELECT 1 FROM crypto_data WHERE symbol = %s AND data_extraction_time = %s
            """
            cursor.execute(select_query, (symbol, data_extraction_time))
            existing_data = cursor.fetchone()

            if not existing_data:
                # Si las cryptos no están para esta fecha y hora, insertar nuevos datos
                insert_query = """
                    INSERT INTO crypto_data (coin_name, symbol, price, price_change, price_movement, data_extraction_time) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (coin_name, symbol, price, price_change, price_movement, data_extraction_time))

        # Confirmar los cambios
        conn.commit()
        print("Datos cargados exitosamente en la tabla crypto_data")

        # Cerrar el cursor
        cursor.close()
    except Exception as e:
        print(f"Error al cargar datos en la base de datos: {e}")


dotenv_path = ''


# Cargar las variables de entorno 
load_dotenv(dotenv_path)

# Obtener las credenciales de la base de datos 
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Url de la API
base_url = "https://api.coinpaprika.com/v1/"

# Obtener los datos del top 10 de criptos
top_10_crypto_data = get_top_10_crypto_data()

# Mostrar los datos en un DataFrame de Pandas
crypto_df = pd.DataFrame(top_10_crypto_data)

try:
    # Establecer la conexión
    conn_string = f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}"
    conn = psycopg2.connect(conn_string)
    print("Conexión exitosa")

    # Cargar datos en la base de datos
    cargar_datos(crypto_df, conn)

    # Cerrar la conexión
    conn.close()
    print("Conexión cerrada")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
