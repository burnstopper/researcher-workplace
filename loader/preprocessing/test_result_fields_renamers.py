from loader.preprocessing.abstract_single_pass_processor import AbstractSinglePassProcessor


class CopingResultFieldsRenamer(AbstractSinglePassProcessor):
    def __init__(self):
        super().__init__("coping", "result fields renamer")


    def _process_single_record_inplace(self, record: dict) -> None:
        record['selfcontrol'] = record['self_control']
        record.pop('self_control')
        record['escaping'] = record['escape_avoidance']
        record.pop('escape_avoidance')
        record['positive_revaluation'] = record['positive_reassessment']
        record.pop('positive_reassessment')


class SpbResultFieldRenamer(AbstractSinglePassProcessor):
    def __init__(self):
        super().__init__("spb", "result fields renamer")

    def _process_single_record_inplace(self, record: dict) -> None:
        record['due_to_self'] = record['duty_to_oneself']
        record.pop('duty_to_oneself')
        record['due_to_others'] = record['due_in_relation_to_others']
        record.pop('due_in_relation_to_others')
