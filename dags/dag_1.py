from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from python_scripts.tweets_pipeline import insert_tweets

with DAG(
        dag_id="data-insertion",
        start_date=datetime(2022, 5, 25),
        schedule_interval="@once",
        catchup=False,
) as dag:

    t1 = PythonOperator(task_id='put_data', python_callable=insert_tweets, dag=dag)

