from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
import os
from dotenv import load_dotenv
import pandas as pd
from Preentrega3 import get_top_10_crypto_data, cargar_datos

dotenv_path = ''

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

# Definir obtener datos
def obtener_datos():
    top_10_crypto_data = get_top_10_crypto_data()
    return pd.DataFrame(top_10_crypto_data)

obtener_datos_task = PythonOperator(
    task_id='obtener_datos',
    python_callable=obtener_datos,
    dag=dag,
)

# Definir cargar datos
def cargar_datos_func(crypto_df, conn):
    cargar_datos(crypto_df, conn)

cargar_datos_task = PythonOperator(
    task_id='cargar_datos',
    python_callable=cargar_datos_func,
    op_kwargs={'crypto_df': obtener_datos_task.output, 'conn': None},  
    dag=dag,
)

# Definir notificacion mail
email_notification = EmailOperator(
    task_id='email_notification',
    to='ejemplomail@gmail.com',
    subject='DAG Execution Failed',
    html_content='The DAG execution has failed and is being retried.',
    dag=dag
)


# Definir las dependencias entre tareas
obtener_datos_task >> cargar_datos_task >> email_notification

