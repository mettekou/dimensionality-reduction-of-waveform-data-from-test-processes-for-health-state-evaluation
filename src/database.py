import datetime
import psycopg

get_all_eol_test_reports_query = """
SELECT part_number, revision_number, process_name, process_version, item_batch_number, item_serial_number, execution_start, variable_path, quantity_value_quantity, NULL
FROM quantity_value
WHERE part_number = %(part_number)s
AND revision_number = %(revision_number)s
AND process_name = ANY(%(process_names)s)
AND execution_start BETWEEN %(start_time)s AND %(end_time)s
UNION ALL
SELECT part_number, revision_number, process_name, process_version, item_batch_number, item_serial_number, execution_start, variable_path, NULL, waveform_value_samples
FROM waveform_value
WHERE part_number = %(part_number)s
AND revision_number = %(revision_number)s
AND process_name = ANY(%(process_names)s)
AND execution_start BETWEEN %(start_time)s AND %(end_time)s;
"""

get_all_eol_test_reports_arguments = {
    "part_number": "AVA0104F",
    "revision_number": "_01",
    "process_names": ["Warm up", "Current Sweep 35bar prop"],
    "start_time": datetime.date(2019, 1, 1),
    "end_time": datetime.date(2019, 1, 14)
}


def get_all_eol_test_reports():
    with psycopg.connect("host=redline dbname=redline user=redline password=redline") as conn:
        with conn.cursor() as cur:
            cur.execute(get_all_eol_test_reports_query,
                        get_all_eol_test_reports_arguments)
            print(cur.fetchone())


get_all_eol_test_reports()
