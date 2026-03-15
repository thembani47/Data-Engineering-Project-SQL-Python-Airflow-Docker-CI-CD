import logging

logger = logging.getLogger(__name__)
table = "yt_api"

def inser_rows(cur, conn, schema, row):
    try:
        if schema == "staging":
            video_id = "video_id"

            cur.execute(f"""INSERT INTO {schema}.{table} (video_id, title, description, published_at, view_count, like_count, comment_count)
                        VALUES (%(video_id)s, %(title)s, %(description)s, %(published_at)s, %(view_count)s, %(like_count)s, %(comment_count)s)""", row)
        else:
            video_id = "Video_id"

            cur.execute(f"""INSERT INTO {schema}.{table} (Video_id, Video_title, Video_description, Video_published_at, Video_view_count, Video_like_count, Video_comment_count)
                        VALUES (%(Video_id)s, %(Video_title)s, %(Video_description)s, %(Video_published_at)s, %(Video_view_count)s, %(Video_like_count)s, %(Video_comment_count)s)""", row)
        
        conn.commit()
        logger.info(f"Inserted video_id: {row[video_id]} into {schema}.{table}")
    except Exception as e:
        logger.error(f"Error inserting video_id: {row[video_id]}")
        raise e
        
def update_rows(cur, conn, schema, row):

    try:
        # staging
        if schema == "staging":
            video_id = "video_id",
            video_title = "title",
            video_description = "description",
            video_published_at = "published_at",
            video_view_count = "view_count",    
            video_like_count = "like_count",
            video_comment_count = "comment_count"   
        # core
        else:
            video_id = "Video_id",
            video_title = "Video_title",
            video_description = "Video_description",
            video_published_at = "Video_published_at",
            video_view_count = "Video_view_count",    
            video_like_count = "Video_like_count",
            video_comment_count = "Video_comment_count"

        cur.execute(f"""UPDATE {schema}.{table}
                    SET "video_title" = %({video_title}s,
                        "video_description" = %({video_description}s,
                        "video_published_at" = %({video_published_at}s,
                        "video_view_count" = %({video_view_count}s,
                        "video_like_count" = %({video_like_count}s,
                        "video_comment_count" = %({video_comment_count}s
                    WHERE "video_id" = %({video_id}s AND "video_published_at" = %({video_published_at}s""", row)
        
        conn.commit()
        logger.info(f"Updated video_id: {row[video_id]} in {schema}.{table}")
    except Exception as e:
        logger.error(f"Error updating video_id: {row[video_id]}")
        raise e
    
def delete_rows(cur, conn, schema, ids_to_delete):
    try:
        ids_to_delete = f"""({', '.join(f"'{id}'" for id in ids_to_delete)})"""
        cur.execute(f"""DELETE FROM {schema}.{table} WHERE "video_id" IN {ids_to_delete}""")
        conn.commit()
        logger.info(f"Deleted video_ids: {ids_to_delete} from {schema}.{table}")
    except Exception as e:
        logger.error(f"Error deleting video_ids: {ids_to_delete}")
        raise e