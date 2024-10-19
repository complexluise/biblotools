import base64
import io
import re
from anthropic import Anthropic
from langsmith import traceable
from pandas import DataFrame
from PIL import Image
from typing import List, Dict, Union

from biblotools.utils import (
    TextExtractor,
    OutputGenerator,
    AIModel
)


class ModelRepository:
    def __init__(self):
        self.text_extractors: Dict[str, TextExtractor] = {}
        self.output_generators: Dict[str, OutputGenerator] = {}
        self.ai_models: Dict[str, AIModel] = {}

    def add_text_extractor(self, name: str, extractor: TextExtractor):
        self.text_extractors[name] = extractor

    def add_output_generator(self, name: str, generator: OutputGenerator):
        self.output_generators[name] = generator

    def add_ai_model(self, name: str, model: AIModel):
        self.ai_models[name] = model

    def get_text_extractor(self, name: str) -> TextExtractor:
        return self.text_extractors.get(name)

    def get_output_generator(self, name: str) -> OutputGenerator:
        return self.output_generators.get(name)

    def get_ai_model(self, name: str) -> AIModel:
        return self.ai_models.get(name)

    def list_text_extractors(self) -> List[str]:
        return list(self.text_extractors.keys())

    def list_output_generators(self) -> List[str]:
        return list(self.output_generators.keys())

    def list_ai_models(self) -> List[str]:
        return list(self.ai_models.keys())


class DefaultTextExtractor(TextExtractor):
    def extract_text(self, image: Image.Image) -> str:
        # Placeholder for OCR logic
        return "Extracted text would appear here"


class CSVGenerator(OutputGenerator):
    def generate(self, data: List[Dict[str, str]]) -> str:
        df = DataFrame(data)
        return df.set_index('Field').T.reset_index(drop=True)

    def save(self, df: DataFrame, filename: str):
        df.to_csv(filename, index=False)


class MARC21Generator(OutputGenerator):
    def generate(self, data: Dict[str, str]) -> str:
        # Placeholder for MARC21 generation logic
        return "MARC21 data would be here"

    def save(self):
        pass


class BIBFRAME2Generator(OutputGenerator):
    def generate(self, data: Dict[str, str]) -> str:
        # Placeholder for BIBFRAME2 generation logic
        return "BIBFRAME2 data would be here"

    def save(self):
        pass


class DefaultAIModel(AIModel):
    def process(self, images: List[Image.Image]) -> Dict[str, str]:
        # Placeholder for AI processing logic
        return {"processed_text": "AI processed text would be here"}


class AnthropicAIModel(AIModel):
    def __init__(self, api_key: str, model_name: str = "claude-3-5-sonnet-20240620"):
        self.client = Anthropic(api_key=api_key)
        self.model_name = model_name

    def process(self, images: List[Image.Image]) -> DataFrame:
        image_data_list = [self._encode_image(img) for img in images]
        message_list = self._create_message_list(image_data_list)
        response = self._generate_response(message_list)
        table: list[dict[str, str]] = self._parse_markdown_table(response)
        return self._table_to_dataframe(table)

    @staticmethod
    def _encode_image(image: Image.Image) -> str:
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    @staticmethod
    def _create_message_list(image_data_list):
        content = []
        for image_data in image_data_list:
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_data
                }
            })
        content.append({"type": "text",
                        "text": "Please extract the information of the book from these images."
                                "Important: include the ISBN. The output should be a markdown table."})
        return [{"role": 'user', "content": content}]

    @traceable
    def _generate_response(self, message_list) -> str:
        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=2048,
            messages=message_list
        )
        return response.content[0].text

    @staticmethod
    def _parse_markdown_table(markdown_text: str) -> List[Dict[str, str]]:
        # Extract the table content
        table_pattern = r'\|(.+)\|'
        table_rows = re.findall(table_pattern, markdown_text, re.MULTILINE)

        if not table_rows:
            return []

        # Split the header and remove leading/trailing whitespace
        headers = [header.strip() for header in table_rows[0].split('|')]

        # Process data rows
        data = []
        for row in table_rows[2:]:  # Skip the header and separator rows
            values = [value.strip() for value in row.split('|')]
            data.append(dict(zip(headers, values)))

        return data

    @staticmethod
    def _table_to_dataframe(data: List[Dict[str, str]]) -> DataFrame:
        # Convert the list of dictionaries to a pandas DataFrame
        df = DataFrame(data)

        # Flatten the DataFrame if it has nested structures
        return df.apply(lambda x: x.explode()).reset_index(drop=True)  # Verificar este correcto el output
