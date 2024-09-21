from typing import List
from PIL import Image
from src.models import ModelRepository


def process_images(repo: ModelRepository, images: List[Image.Image], ai_model_name: str, output_format: str) -> str:
    ai_model = repo.get_ai_model(ai_model_name)
    processed_data = ai_model.process(images)

    generator = repo.get_output_generator(output_format)
    result = generator.generate(processed_data)

    return result


def configure_model_repository() -> ModelRepository:
    from src.models import AnthropicAIModel, CSVGenerator, MARC21Generator, BIBFRAME2Generator
    import os

    repo = ModelRepository()

    API_KEY = os.getenv("ANTHROPIC_KEY")
    if API_KEY:
        repo.add_ai_model("anthropic", AnthropicAIModel(API_KEY, "claude-3-5-sonnet-20240620"))

    repo.add_output_generator("CSV", CSVGenerator())
    repo.add_output_generator("MARC21", MARC21Generator())
    repo.add_output_generator("BIBFRAME2", BIBFRAME2Generator())

    return repo
