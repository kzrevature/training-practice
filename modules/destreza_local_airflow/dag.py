from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG, task

with DAG(dag_id="destreza_dag") as dag:
    task_1 = PythonOperator(
        task_id="t1", python_callable=print, op_args="Hello World 1!"
    )
    task_2 = BashOperator(task_id="t2", bash_command="echo 'hello world two.'")

    @task()
    def task_3():
        print("HeLLo wORld 3?")

    task_1 >> task_2 >> task_3()
