import os
import click
from PIL import Image
from src.use_cases import configure_model_repository, process_images


@click.command()
@click.argument('image_folder', type=click.Path(exists=True))
@click.option('--output_file', default='output.csv', help='The output file to store the extracted information.')
def main(image_folder, output_file):
    repo = configure_model_repository()

    # Get list of image paths in the specified folder
    image_paths = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if
                   f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not image_paths:
        print(f"No images found in folder: {image_folder}")
        return

    # Load images
    images = [Image.open(path) for path in image_paths]

    # Process images
    result = process_images(repo, images, "anthropic", "CSV")

    # Write result to file
    with open(output_file, mode='w', newline='') as file:
        file.write(result)

    print(f"Extracted information written to {output_file}")


if __name__ == "__main__":
    main()