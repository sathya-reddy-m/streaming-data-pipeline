from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow import DAG
from airflow import LoggingMixin
from airflow.models import Variable

logger = LoggingMixin()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.today().strftime('%Y-%m-%d'),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG('e2e_test',default_args=default_args, schedule_interval='0 * * * *', catchup=False)

env_variables = Variable.get("environment_variables", deserialize_json=True)

cohort = env_variables["cohort"]
e2e_test_command = """
export TRAINING_COHORT={cohort} && ~/e2e.sh
""".format(cohort=cohort)

t1 = BashOperator(
    task_id='execute_test',
    bash_command=e2e_test_command,
    dag=dag)
