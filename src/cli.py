import os
import click
from PIL import Image
from itertools import groupby
from typing import List, Dict
import pandas as pd
from src.use_cases import configure_model_repository, process_images


def group_images_by_book(image_paths: List[str]) -> Dict[str, List[str]]:
    """
    Groups image paths by book based on a naming convention.

    The naming convention is as follows:
    - Images for the same book should have the same prefix, followed by an underscore and a number.
    - Example: "book1_1.jpg", "book1_2.jpg" belong to the same book.

    Args:
        image_paths (List[str]): A list of image file paths.

    Returns:
        Dict[str, List[str]]: A dictionary where keys are book identifiers and values are lists of image paths.

    Example:
        >>> paths = ["/path/book1_1.jpg", "/path/book1_2.jpg", "/path/book2_1.jpg"]
        >>> group_images_by_book(paths)
        {'book1': ['/path/book1_1.jpg', '/path/book1_2.jpg'], 'book2': ['/path/book2_1.jpg']}
    """

    def get_book_key(path):
        return os.path.basename(path).split('_')[0]

    sorted_paths = sorted(image_paths, key=get_book_key)
    return {book: list(paths) for book, paths in groupby(sorted_paths, key=get_book_key)}


@click.command()
@click.argument('image_folder', type=click.Path(exists=True))
@click.option('--output_file', default='output.csv', help='The output file to store the extracted information.')
@click.option('--output_format', default='CSV', type=click.Choice(['CSV', 'TABLE']), help='The output format for the extracted information.')
def main(image_folder: str, output_file: str, output_format: str):
    """
    Process book images and extract information.

    This CLI tool processes images of books, potentially multiple images per book,
    and extracts relevant information using AI. The extracted data is then saved
    to a file in the specified format.

    Images should follow this naming convention:
    - Images for the same book should have the same prefix, followed by an underscore and a number.
    - Example: "book1_1.jpg", "book1_2.jpg" belong to the same book.

    Args:
        image_folder (str): Path to the folder containing book images.
        output_file (str): Path to the output file. Defaults to 'output.csv'.
        output_format (str): Format of the output file. Can be 'CSV' or 'TABLE'. Defaults to 'CSV'.

    Example usage:
        $ python cli.py /path/to/images --output_file=books_info.csv --output_format=CSV
    """
    repo = configure_model_repository()

    # Get list of image paths in the specified folder
    image_paths = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if
                   f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not image_paths:
        print(f"No images found in folder: {image_folder}")
        return

    # Group images by book
    books = group_images_by_book(image_paths)

    all_results = []
    for book_id, book_image_paths in books.items():
        print(f"Processing book: {book_id}")
        book_images = [Image.open(path) for path in book_image_paths]
        result = process_images(repo, book_images, 'Antropic - Claude Sonnet 3.5', output_format)
        all_results.append(result)

    repo.get_output_generator(output_format).save(all_results)
    # Combine results and write to file
    if output_format == 'TABLE':
        combined_result = pd.concat(all_results, ignore_index=True)
        combined_result.to_csv(output_file, index=False)
    else:
        combined_result = "\n".join([result.to_csv(index=False) for result in all_results])
        with open(output_file, mode='w', newline='') as file:
            file.write(combined_result)

    print(f"Extracted information for {len(books)} books written to {output_file}")


if __name__ == "__main__":
    main()
