from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import os
from dotenv import load_dotenv
import pandas as pd
from Preentrega3 import get_top_10_crypto_data, cargar_datos

# Especificar la ruta completa al archivo .env
dotenv_path = 'C:\\Users\gaspi\\Desktop\\Airflow_final\\.env'

# Cargar las variables de entorno desde el archivo .env
load_dotenv(dotenv_path)

# Definir los argumentos del DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 26),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
}

# Definir el DAG
dag = DAG(
    'crypto_etl_dag',
    default_args=default_args,
    description='ETL DAG for cryptocurrency data',
    schedule_interval='@daily',
)

# Definir la tarea de obtener datos
def obtener_datos():
    top_10_crypto_data = get_top_10_crypto_data()
    return pd.DataFrame(top_10_crypto_data)

obtener_datos_task = PythonOperator(
    task_id='obtener_datos',
    python_callable=obtener_datos,
    dag=dag,
)

# Definir la tarea de cargar datos
def cargar_datos_func(crypto_df, conn):
    cargar_datos(crypto_df, conn)

cargar_datos_task = PythonOperator(
    task_id='cargar_datos',
    python_callable=cargar_datos_func,
    op_kwargs={'crypto_df': obtener_datos_task.output, 'conn': None},  
    dag=dag,
)

# Definir las dependencias entre tareas
obtener_datos_task >> cargar_datos_task

