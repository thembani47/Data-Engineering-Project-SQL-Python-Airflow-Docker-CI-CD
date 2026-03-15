from data_utils import get_conn_cusor, create_schema, create_table, get_video_ids, close_conn_cursor
from data_modification import inser_rows, update_rows, delete_rows
from data_loading import load_data
from data_transformation import transform_data

import logging
from airflow.decorators import task

logger = logging.getLogger(__name__)
table = "yt_api"

@task
def staging_table():

    schema = "staging"

    try:

        conn, cur = get_conn_cusor()

        YT_data = load_data()

        create_schema(schema)
        create_table(schema)

        table_ids = get_video_ids(cur, schema)

        for row in YT_data:

            if len(table_ids) == 0:
                inser_rows(cur, conn, schema, row)
            
            else:
                if row["video_id"] in table_ids:
                    update_rows(cur, conn, schema, row)
                else:
                    inser_rows(cur, conn, schema, row)

        ids_in_json = [row["video_id"] for row in YT_data]
        ids_to_delete = set(table_ids) - ids_in_json

        if ids_to_delete:
            delete_rows(cur, conn, schema, ids_to_delete)

        logger.info(f"Staging table {schema}.{table} updated successfully.")

    except Exception as e:
        logger.error(f"Error updating staging table: {e}")
        raise e
    finally:
        close_conn_cursor(conn, cur)



