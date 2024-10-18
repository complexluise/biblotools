import streamlit as st
from PIL import Image
import pandas as pd
from src.use_cases import configure_model_repository, process_images


def upload_images():
    uploaded_files = st.file_uploader("Choose image files", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    images = []
    if uploaded_files:
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file)
            images.append(image)
            st.image(image, caption=f"Uploaded Image: {uploaded_file.name}", use_column_width=True)
    return images


def main():
    st.title("Library AI Showcase")

    repo = configure_model_repository()

    images = upload_images()

    if images:
        ai_model_name = st.selectbox(
            "Select AI Model",
            repo.list_ai_models()
        )

        output_format = st.selectbox(
            "Select output format",
            repo.list_output_generators()
        )

        if st.button("Generate"):
            results = process_images(repo, images, ai_model_name, output_format)

            # Assuming results is a list of dictionaries
            df = pd.DataFrame(results)
            st.table(df)


if __name__ == "__main__":
    main()
