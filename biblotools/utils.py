from abc import ABC, abstractmethod
from PIL import Image
from typing import List, Dict


class TextExtractor(ABC):
    @abstractmethod
    def extract_text(self, image: Image.Image) -> str:
        pass


class OutputGenerator(ABC):
    @abstractmethod
    def generate(self, data: Dict[str, str]):
        pass

    @abstractmethod
    def save(self, *args, **kwargs):
        pass


class AIModel(ABC):
    @abstractmethod
    def process(self, images: List[Image.Image]) -> Dict[str, str]:
        pass


class UseCase(ABC):
    def __init__(self, model_repository):
        self.repo = model_repository

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
