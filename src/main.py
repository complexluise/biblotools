import base64
import os
import csv
import click
from anthropic import Anthropic

PROMPT = "Please extract the information of the book from these images. Important: include the ISBN of the book. The Output is a JSON."

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

@click.command()
@click.argument('image_folder', type=click.Path(exists=True))
@click.option('--output_csv', default='output.csv', help='The output CSV file to store the extracted information.')
def main(image_folder, output_csv):
    API_KEY = os.getenv("ANTHROPIC_KEY")
    if not API_KEY:
        print("Error: ANTHROPIC_KEY environment variable not set.")
        return

    client = Anthropic(api_key=API_KEY)
    MODEL_NAME = "claude-3-5-sonnet-20240620"

    # Get list of image paths in the specified folder
    image_paths = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not image_paths:
        print(f"No images found in folder: {image_folder}")
        return

    image_data_list = []
    for image_path in image_paths:
        binary_data = read_image(image_path)
        base64_string = encode_image_to_base64(binary_data)
        image_data_list.append(base64_string)

    message_list = create_message_list(image_data_list, PROMPT)
    response = generate_response(client, MODEL_NAME, message_list)

    # Write response to CSV file
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Image', 'Extracted Information'])
        for i, image_path in enumerate(image_paths):
            writer.writerow([image_path, response])

    print(f"Extracted information written to {output_csv}")

if __name__ == "__main__":
    main()
