import datetime
import pandas as pd
from sqlalchemy import create_engine

values_query = """
SELECT part_number, revision_number, item_batch_number, item_serial_number, process_name, execution_start, array_to_string(variable_path, '/') AS variable_path, quantity_value_quantity
FROM quantity_value
WHERE part_number = ANY(%(part_numbers)s)
AND revision_number = ANY(%(revision_number)s)
AND process_name = ANY(%(process_names)s)
AND execution_start BETWEEN %(start_time)s AND %(end_time)s
ORDER BY part_number, revision_number, item_batch_number, item_serial_number, process_name, execution_start
"""

failures_query = """
SELECT DISTINCT part_number, revision_number, item_batch_number, item_serial_number, process_name, execution_start, false AS "ok"
FROM failure
WHERE part_number = ANY(%(part_numbers)s)
AND revision_number = ANY(%(revision_number)s)
AND process_name = ANY(%(process_names)s)
AND execution_start BETWEEN %(start_time)s AND %(end_time)s
UNION ALL
SELECT DISTINCT part_number, revision_number, item_batch_number, item_serial_number, process_name, execution_start, true as "ok"
FROM execution
WHERE part_number = ANY(%(part_numbers)s)
AND revision_number = ANY(%(revision_number)s)
AND process_name = ANY(%(process_names)s)
AND execution_start BETWEEN %(start_time)s AND %(end_time)s
AND NOT EXISTS
    (SELECT FROM failure
    WHERE part_number = execution.part_number
    AND revision_number = execution.revision_number
    AND item_batch_number = execution.item_batch_number
    AND item_serial_number = execution.item_serial_number
    AND process_name = execution.process_name
    AND process_version = execution.process_version
    AND equipment_name = execution.equipment_name
    AND execution_start = execution.execution_start)
ORDER BY part_number, revision_number, item_batch_number, item_serial_number, process_name, execution_start
"""

query_arguments = {
    "part_numbers": ["AVA0104F", "TT_Type 1"],
    "revision_number": ["_01", "A01", ""],
    "process_names": ["Current Sweep 35bar prop"],
    "start_time": datetime.date(2018, 12, 1),
    "end_time": datetime.date(2019, 2, 28)
}


def load(connection_string):
    engine = create_engine(connection_string)
    values = pd.pivot_table(pd.read_sql_query(values_query, engine, params=query_arguments),
                            index=["part_number", "revision_number", "item_batch_number",
                                   "item_serial_number", "process_name", "execution_start"],
                            columns="variable_path",
                            values="quantity_value_quantity").reset_index()
    failures = pd.read_sql_query(
        failures_query, engine, params=query_arguments)
    return values.merge(failures, how="outer")
