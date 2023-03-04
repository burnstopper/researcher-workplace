class TestInfo:
    test_id: int
    respondent_id: int
    date_time: int
    quiz_id: str

    @staticmethod
    def from_json(json: dict):
        ti = TestInfo()
        ti.date_time = json['date_time']
        ti.quiz_id = json['quiz_id']
        ti.respondent_id = json['respondent_id']
        ti.test_id = json['result_id']
        return ti
    
    
    def copy(self):
        ti = TestInfo()
        ti.date_time = self.date_time
        ti.test_id = self.test_id
        ti.respondent_id = self.respondent_id
        ti.quiz_id = self.quiz_id
        return ti


from loader.service_loader.adopted_distress_test_service import AdoptedDistressTestService
from loader.service_loader.test_service import TestService, DefaultTestService
from loader.service_loader.questionnary_service import QuestionnaryServiceStub

__all__ = [
    "TestInfo",
    "TestService",
    "DefaultTestService",
    "AdoptedDistressTestService",
    "QuestionnaryServiceStub"
]
