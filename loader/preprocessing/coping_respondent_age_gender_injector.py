from loader.preprocessing.abstract_single_pass_processor import AbstractSinglePassProcessor
from loader.service_loader.questionnary_service import QuestionnaryService


class CopingRespondentAgeGenderInjector(AbstractSinglePassProcessor):
    def __init__(self, questionary_service: QuestionnaryService):
        super().__init__("coping", "age and gender fields injector")
        self._service = questionary_service


    _service: QuestionnaryService


    def _process_single_record_inplace(self, record: dict):
        respondent_id = record['respondent_id']
        record['age'] = self._service.get_respondent_age(respondent_id)
        record['gender'] = self._service.get_respondent_gender(respondent_id)
