from typing import List
from PIL import Image
from biblotools.models import AnthropicAIModel, ModelRepository, CSVGenerator


def process_images(repo: ModelRepository, images: List[Image.Image], ai_model_name: str, output_format: str):
    ai_model = repo.get_ai_model(ai_model_name)
    processed_data = ai_model.process(images)

    return repo.get_output_generator(output_format).generate(processed_data)


def configure_model_repository() -> ModelRepository:
    import os

    repo = ModelRepository()

    API_KEY = os.getenv("ANTHROPIC_KEY")
    if API_KEY:
        repo.add_ai_model("Antropic - Claude Sonnet 3.5", AnthropicAIModel(API_KEY, "claude-3-5-sonnet-20240620"))

    repo.add_output_generator("CSV", CSVGenerator())
    return repo
