# Ten kod demonstruje użycie operatora BranchDateTimeOperator w Airflow, który umożliwia warunkowe sterowanie przepływem zadań w zależności od daty i czasu, w którym zadanie jest wykonywane.

from __future__ import annotations

import pendulum

from airflow.models.dag import DAG
from airflow.operators.datetime import BranchDateTimeOperator
from airflow.operators.empty import EmptyOperator

dag1 = DAG(
    dag_id="example_branch_datetime_operator",
    start_date=pendulum.datetime(2024, 5, 15, tz="UTC"),
    catchup=True,
    tags=["a"],
    schedule=None,
)

empty_task_11 = EmptyOperator(task_id="date_in_range", dag=dag1)
empty_task_21 = EmptyOperator(task_id="date_outside_range", dag=dag1)

cond1 = BranchDateTimeOperator(
    task_id="datetime_branch",
    follow_task_ids_if_true=["date_in_range"],
    follow_task_ids_if_false=["date_outside_range"],
    target_upper=pendulum.datetime(2024, 12, 10, 15, 0, 0),
    target_lower=pendulum.datetime(2024, 5, 10, 14, 0, 0),
    dag=dag1,
)

cond1 >> [empty_task_11, empty_task_21]

dag2 = DAG(
    dag_id="example_branch_datetime_operator_2",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    tags=["a"],
    schedule=None,
)

empty_task_12 = EmptyOperator(task_id="date_in_range", dag=dag2)
empty_task_22 = EmptyOperator(task_id="date_outside_range", dag=dag2)

cond2 = BranchDateTimeOperator(
    task_id="datetime_branch",
    follow_task_ids_if_true=["date_in_range"],
    follow_task_ids_if_false=["date_outside_range"],
    target_upper=pendulum.time(0, 0, 0),
    target_lower=pendulum.time(13, 0, 0),
    dag=dag2,
)

cond2 >> [empty_task_12, empty_task_22]

dag3 = DAG(
    dag_id="example_branch_datetime_operator_3",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    tags=["a"],
    schedule=None,
)

empty_task_13 = EmptyOperator(task_id="date_in_range", dag=dag3)
empty_task_23 = EmptyOperator(task_id="date_outside_range", dag=dag3)

cond3 = BranchDateTimeOperator(
    task_id="datetime_branch",
    use_task_logical_date=True, # Zamiast bazować na bieżącej dacie systemowej, branchowanie opiera się na logicznej dacie zadania (czyli dacie przypisanej w harmonogramie Airflow, a nie rzeczywistym czasie jego wykonania).
    follow_task_ids_if_true=["date_in_range"],
    follow_task_ids_if_false=["date_outside_range"],
    target_upper=pendulum.datetime(2024, 10, 10, 15, 0, 0),
    target_lower=pendulum.datetime(2024, 5, 10, 14, 0, 0),
    dag=dag3,
)

cond3 >> [empty_task_13, empty_task_23]
