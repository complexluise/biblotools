import base64
import os
from anthropic import Anthropic


def read_image(file_path):
    with open(file_path, "rb") as image_file:
        return image_file.read()


def encode_image_to_base64(binary_data):
    base_64_encoded_data = base64.b64encode(binary_data)
    return base_64_encoded_data.decode('utf-8')


def create_message_list(image_data_list, prompt):
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
    content.append({"type": "text", "text": prompt})
    return [{"role": 'user', "content": content}]


def generate_response(client, model_name, message_list):
    response = client.messages.create(
        model=model_name,
        max_tokens=2048,
        messages=message_list
    )
    return response.content[0].text


def main():
    API_KEY = os.getenv("ANTHROPIC_KEY")
    client = Anthropic(api_key=API_KEY)
    MODEL_NAME = "claude-3-5-sonnet-20240620"
    IMAGE_PATHS = [
        "image/WhatsApp Image 2024-08-05 at 23.53.32_6c7a93e6.jpg",
        "image/WhatsApp Image 2024-08-05 at 23.54.04_56c2bab1.jpg",
    ]
    PROMPT = ("Please extract the information of the book from these images.\n"
              "Important: include the ISBN of the book.\n"
              "The Output is a Json")

    image_data_list = []
    for image_path in IMAGE_PATHS:
        binary_data = read_image(image_path)
        base64_string = encode_image_to_base64(binary_data)
        image_data_list.append(base64_string)

    message_list = create_message_list(image_data_list, PROMPT)
    response = generate_response(client, MODEL_NAME, message_list)
    print(response)


if __name__ == "__main__":
    main()
