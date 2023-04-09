import datetime
import pytz

from loader.preprocessing.abstract_single_pass_processor import AbstractSinglePassProcessor


class TimestampToDatetimeRecoder(AbstractSinglePassProcessor):
    def __init__(self, test_name: str):
        super().__init__(test_name, "timestamp to datetime record")


    def _process_single_record_inplace(self, record: dict) -> None:
        date_time_timestamp = record['date_time']
        date_time = datetime.datetime.fromtimestamp(date_time_timestamp, pytz.UTC)
        record['date_time'] = date_time
