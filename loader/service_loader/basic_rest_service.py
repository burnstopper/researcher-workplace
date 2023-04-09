import json
import logging
from typing import Union

import requests
import requests.auth

from loader.service_loader.errors import ServiceError


STATUS_CODE_OK = 200
STATUS_CODE_UNAUTHORIZED = 401
STATUS_CODE_FORBIDDEN = 403


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = "Bearer " + self.token
        return r


class BasicRestService:
    def __init__(self, host: str, port: int, token: str):
        self._authorization = BearerAuth(token)
        self._host = host
        self._port = port
        self._logger = logging.getLogger(f"loader.{__class__.__name__}")


    def make_request(self, url_path: str, params: dict) -> Union[list, dict]:
        try:
            response = requests.get(f"http://{self._host}:{self._port}/{url_path}",
                                    auth=self._authorization,
                                    params=params,
                                    timeout=10)
        except IOError as e:
            self._logger.error(f"Request failed due to IOError: {e}")
            return {}
        if response.status_code in (STATUS_CODE_UNAUTHORIZED, STATUS_CODE_FORBIDDEN):
            self._logger.error(f"Auth token provided for service on addr {self._host}:{self._port} is not valid")
            raise ServiceError(response.status_code)
        elif response.status_code != STATUS_CODE_OK:
            self._logger.error(f"Request {response.request.method} {response.request.url}"
                               f"failed with http status code: {response.status_code}")
            raise ServiceError(response.status_code)
        try:
            res = response.json()
        except Exception as e:
            self._logger.error(f"Failed to parse response: {e}")
            res = {}
        return res
