from airflow import DAG
import pendulum
from api.videos_stats import get_channel_playlistid, get_video_ids, extracted_video_data, save_to_json
from datetime import timedelta, datetime

# Define local timezone
local_tz = pendulum.timezone("Africa/Johannesburg")

# Define default arguments for the DAG
default_args = {
    "owner": "thembani",
    "depends_on_past": False,
    "email_on_failure": False,
    "email": ["thembani@example.com"],
    "max_active_runs": 1,
    "dagrun_timeout": timedelta(minutes=60),
    "start_date": datetime(2026, 3, 15, tzinfo=local_tz)
}

with DAG(
    dag_id="youtube_data_pipeline",
    default_args=default_args,
    description="A DAG to extract YouTube channel data and save it to a JSON file",
    schedule="0 14 * * *",  # Run daily at 14:00 local time
    catchup=False
) as dag:

    playlist_id = get_channel_playlistid()
    video_ids = get_video_ids(playlist_id)
    extracted_data = extracted_video_data(video_ids)
    save_to_json_task = save_to_json(extracted_data)

    # Set task dependencies
    playlist_id >> video_ids >> extracted_data >> save_to_json_task