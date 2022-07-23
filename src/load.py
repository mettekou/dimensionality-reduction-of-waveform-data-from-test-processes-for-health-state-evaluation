import datetime
import numpy as np
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

quantity_value_failed_query = """
SELECT part_number, revision_number, item_batch_number, item_serial_number, process_name, execution_start, array_to_string(variable_path, '/') AS variable_path, quantity_value_quantity
FROM quantity_value_failed_sample;
"""

quantity_value_passed_query = """
SELECT part_number, revision_number, item_batch_number, item_serial_number, process_name, execution_start, array_to_string(variable_path, '/') AS variable_path, quantity_value_quantity
FROM quantity_value_passed_sample;
"""

waveform_value_failed_query = """
SELECT part_number, revision_number, item_batch_number, item_serial_number, process_name, execution_start, array_to_string(variable_path, '/') AS variable_path, waveform_value_samples, waveform_value_length
FROM waveform_value_failed_sample
WHERE variable_path = '{"0/Pressure/M_RIO_PRS_A"}';
"""

waveform_value_passed_query = """
SELECT part_number, revision_number, item_batch_number, item_serial_number, process_name, execution_start, array_to_string(variable_path, '/') AS variable_path, waveform_value_samples, waveform_value_length
FROM waveform_value_passed_sample
WHERE variable_path = '{"0/Pressure/M_RIO_PRS_A"}';
"""

passed_executions_query = """
SELECT setseed(0.42);
SELECT e.part_number, e.revision_number, e.item_batch_number, e.item_serial_number, e.process_name, e.process_version, e.execution_start, e.equipment_name
INTO execution_failed_sample
FROM execution e
WHERE part_number = 'TT_Type 1' AND revision_number = ''
AND execution_start BETWEEN '2021-01-01' AND '2022-07-01'
AND process_name = 'Current_Sweep'
AND NOT EXISTS
    (SELECT
     FROM failure f
     WHERE e.part_number = f.part_number
     AND e.revision_number = f.revision_number
     AND e.process_name = f.process_name
     AND e.process_version = f.process_version
     AND e.item_batch_number = f.item_batch_number
     AND e.item_serial_number = f.item_serial_number
     AND e.execution_start = f.execution_start
     AND e.equipment_name = f.equipment_name)
ORDER BY random()
LIMIT 20942;
"""

failed_executions_query = """
WITH
    f AS (SELECT DISTINCT part_number, revision_number, item_batch_number, item_serial_number, process_name, process_version, execution_start, equipment_name
    FROM failure
    WHERE part_number = 'TT_Type 1' AND revision_number = '' AND process_name = 'Current_Sweep'
    AND execution_start BETWEEN '2021-01-01' AND '2022-07-01')
SELECT *
INTO waveform_value_sample_failed
FROM waveform_value
INNER JOIN f USING (part_number, revision_number, item_batch_number, item_serial_number, process_name, process_version, execution_start, equipment_name);
"""

query_arguments = {
    "part_numbers": ["TT_Type 1"],
    "revision_number": [""],
    "process_names": ["Current_Sweep"],
    "variable_path": ["0/Current/M_TSIM_CUR_I1","0/Pressure/M_RIO_PRS_A","0/Temperature/M_RIO_TMP_Temp"],
    "start_time": datetime.date(2021, 1, 1),
    "end_time": datetime.date(2022, 7, 1)
}

def load(connection_string):
    engine = create_engine(connection_string)
    failed = pd.pivot_table(pd.read_sql_query(quantity_value_failed_query, engine),
                            index=["part_number", "revision_number", "item_batch_number",
                                   "item_serial_number", "process_name", "execution_start"],
                            columns="variable_path",
                            values="quantity_value_quantity").reset_index()
    failed["ok"] = False
    passed = pd.pivot_table(pd.read_sql_query(quantity_value_passed_query, engine),
                            index=["part_number", "revision_number", "item_batch_number",
                                   "item_serial_number", "process_name", "execution_start"],
                            columns="variable_path",
                            values="quantity_value_quantity").reset_index()
    passed["ok"] = True
    return pd.concat([failed, passed])

def load_waveform_values(connection_string):
    x = []
    y = []
    with psycopg2.connect(connection_string) as connection:
        with connection.cursor() as cursor:
            cursor.execute(waveform_value_passed_query, query_arguments)
            for record in cursor:
                _, _, _, _, _, _, _, waveform_value_samples, _ = record
                x.append(waveform_value_samples)
                y.append(True)
            cursor.execute(waveform_value_failed_query, query_arguments)
            for record in cursor:
                _, _, _, _, _, _, _, waveform_value_samples, _ = record
                x.append(waveform_value_samples)
                y.append(False)
    length = max(map(len, x))

    return np.array([xi+[0.0]*(length-len(xi)) for xi in x]), np.array(y)
