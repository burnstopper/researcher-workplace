import logging
from typing import Dict, Type, Any, Optional

from loader.errors import BadConfig
from loader.preprocessing import *
from loader.service_loader import *
from loader.storage import *
from loader.test_results_download_controller import TestResultsDownloadController
from loader.tools import extract_service_token, get_service_host_and_port

class TestImplementationHolder():
    def __init__(self):
        self._logger = logging.getLogger("loader")

    def setup(self, config: Dict):
        try:
            self._setup_impl(config)
            self._download_controller = TestResultsDownloadController(self.service)
        except KeyError as e:
            raise BadConfig(e.args[0], missing=True)
        except ValueError as e:
            raise BadConfig(e.args[0], misconfigured=True)
        except Exception as e:
            self._logger.error(f"Cannot setup TestImplementationHolder due to error: {e}")
            raise BadConfig("")


    @property
    def service(self) -> TestService:
        return self._service


    @property
    def test_result_record(self) -> Type:
        return self._test_result_record
    

    @property
    def preprocessing_pipeline(self) -> Pipeline:
        return self._preprocessing_pipeline


    @property
    def download_controller(self) -> TestResultsDownloadController:
        return self._download_controller


    def _set_service(self, service: TestService):
        self._service = service


    def _set_test_result_record(self, result_record: Type):
        self._test_result_record = result_record


    def _set_preprocessing_pipeline(self, pipeline: Pipeline):
        self._preprocessing_pipeline = pipeline


    def _setup_impl(self, config: Dict):
        raise NotImplementedError(f"TestImplementationHolder.setup_impl is not implemented in {self.__class__}")


class BurnoutTestImplementationHolder(TestImplementationHolder):
    def _setup_impl(self, config: Dict[str, Any]):
        host, port = get_service_host_and_port(config['burnout_service'])
        token = extract_service_token('burnout', config)
        self._set_service(DefaultTestService(host, port, token))

        self._set_preprocessing_pipeline(Pipeline(
            BurnoutCategorialFieldsEncoder(),
            BurnoutRelativeScoreInjector(),
            TimestampToDatetimeRecoder("burnout"),
        ))

        self._set_test_result_record(BurnoutTestRecord)


class DistressTestImplementationHolder(TestImplementationHolder):
    def _setup_impl(self, config: Dict[str, Any]):
        host, port = get_service_host_and_port(config['distress_service'])
        token = extract_service_token('distress', config)
        self._set_service(AdoptedDistressTestService(host, port, token))

        self._set_preprocessing_pipeline(Pipeline(
            DistressCategorialFieldsEncoder(),
            DistressRelativeScoreInjector(),
            TimestampToDatetimeRecoder("distress"),
        ))

        self._set_test_result_record(DistressTestRecord)


class CopingTestImplementationHolder(TestImplementationHolder):
    def _setup_impl(self, config: Dict[str, Any]):
        host, port = get_service_host_and_port(config['coping_service'])
        token = extract_service_token('coping', config)
        self._set_service(DefaultTestService(host, port, token))

        # FIXME: currently only fake implementaion of questionnary service available
        questionnary_service = QuestionnaryServiceStub()
        self._set_preprocessing_pipeline(Pipeline(
            CopingResultFieldsRenamer(),
            CopingRespondentAgeGenderInjector(questionnary_service),
            CopingTScoreCalculator(),
            CopingCategorialFieldsEncoder(),
            TimestampToDatetimeRecoder("coping"),
        ))

        self._set_test_result_record(CopingTestRecord)


class SpbTestImplementationHolder(TestImplementationHolder):
    def _setup_impl(self, config: Dict[str, Any]):
        host, port = get_service_host_and_port(config['spb_service'])
        token = extract_service_token('spb', config)
        self._set_service(DefaultTestService(host, port, token))

        self._set_preprocessing_pipeline(Pipeline(
            SpbResultFieldRenamer(),
            SpbCategorialFieldsEncoder(),
            TimestampToDatetimeRecoder("spb"),
        ))

        self._set_test_result_record(SpbTestRecord)


class TestImplementationFactory:
    def create(self, name: str, config: Dict[str, Any]) -> Optional[TestImplementationHolder]:
        holder = TestImplementationFactory._select_concrete_holder(name)
        if not holder:
            return holder
        holder.setup(config)
        return holder
    

    @staticmethod
    def _select_concrete_holder(name: str) -> Optional[TestImplementationHolder]:
        if name == "burnout":
            return BurnoutTestImplementationHolder()
        elif name == "distress":
            return DistressTestImplementationHolder()
        elif name == "coping":
            return CopingTestImplementationHolder()
        elif name == "spb":
            return SpbTestImplementationHolder()
        else:
            return None
