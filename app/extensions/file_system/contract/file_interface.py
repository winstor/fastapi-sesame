from abc import ABCMeta, abstractmethod
from typing import List
from fastapi import Depends


class FileInterface(metaclass=ABCMeta):
    config = {}

    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def put(self, path: str, content: str):
        raise NotImplementedError

    @abstractmethod
    def get(self, path: str):
        raise NotImplementedError

    @abstractmethod
    def delete(self, path: str):
        raise NotImplementedError

    @abstractmethod
    def url(self, path: str):
        raise NotImplementedError
