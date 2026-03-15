from airflow.providers.postgres.hooks.postgres import PostgresHook
from pycopg2.extras import RealDictCursor

table = "yt_api"

def get_conn_cusor():
    hook = PostgresHook(postgres_conn_id="postgres_db_yt_elt", database="elt_db")
    conn = hook.get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    return conn, cur

def close_conn_cursor(conn, cur):
    cur.close()
    conn.close()

def create_schema(schema):

    conn, cur = get_conn_cusor()

    schema_sql = f"CREATE SCHEMA IF NOT EXISTS {schema};"

    cur.execute(schema_sql)
    conn.commit()

    close_conn_cursor(conn, cur)

def create_table(schema):

    conn, cur = get_conn_cusor()

    if schema == "staging":
        table_sql = f"""
            CREATE TABLE IF NOT EXISTS {schema}.{table} (
                video_id VARCHAR(255) PRIMARY KEY,
                title TEXT,
                description TEXT,
                published_at TIMESTAMP,
                view_count INTEGER,
                like_count INTEGER,
                comment_count INTEGER
            );
        """
    else:
        table_sql = f"""
            CREATE TABLE IF NOT EXISTS {schema}.{table} (
                video_id VARCHAR(255) PRIMARY KEY,
                title TEXT,
                description TEXT,
                published_at TIMESTAMP,
                view_count INTEGER,
                like_count INTEGER,
                comment_count INTEGER
            );
        """

    cur.execute(table_sql)
    conn.commit()

    close_conn_cursor(conn, cur)

def get_video_ids(cur, schema):

    cur.execute(f"""SELECT "video_id" FROM {schema}.{table};""")
    ids = cur.fetchall()

    video_ids = [row["video_id"] for row in ids]

    return video_ids