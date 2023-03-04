class QuestionnaryService:
    def get_respondent_age(self, respondent_id: int) -> int:
        raise NotImplementedError("Questionnary service is still not implemented")
    
    def get_respondent_gender(self, respondent_id: int) -> str:
        raise NotImplementedError("Questionnary service is still not implemented")


class QuestionnaryServiceStub(QuestionnaryService):
    def get_respondent_age(self, _: int) -> int:
        return 21
    
    def get_respondent_gender(self, _) -> str:
        return 'm'
