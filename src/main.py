import base64
import os

from anthropic import Anthropic


def read_image(file_path):
    with open(file_path, "rb") as image_file:
        return image_file.read()


def encode_image_to_base64(binary_data):
    base_64_encoded_data = base64.b64encode(binary_data)
    return base_64_encoded_data.decode('utf-8')


def create_message_list(base64_string, prompt):
    return [
        {
            "role": 'user',
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": base64_string}},
                {"type": "text", "text": prompt}
            ]
        }
    ]


def generate_sonnet(client, model_name, message_list):
    response = client.messages.create(
        model=model_name,
        max_tokens=2048,
        messages=message_list
    )
    return response.content[0].text


def main():
    API_KEY = os.getenv("ANTHROPIC_KEY")
    client = Anthropic(api_key=API_KEY)
    MODEL_NAME = "claude-3-opus-20240229"
    IMAGE_PATH = "image/WhatsApp Image 2024-08-05 at 23.53.32_6c7a93e6.jpg"
    PROMPT = "Please write a CSV file with the image, lets think in a library catalog ontology"

    binary_data = read_image(IMAGE_PATH)
    base64_string = encode_image_to_base64(binary_data)
    message_list = create_message_list(base64_string, PROMPT)
    sonnet = generate_sonnet(client, MODEL_NAME, message_list)
    print(sonnet)


if __name__ == "__main__":
    main()
