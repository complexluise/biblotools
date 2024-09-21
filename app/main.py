import streamlit as st
from PIL import Image
from src.use_cases import configure_model_repository, process_images


def upload_image():
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        return image
    return None


def main():
    st.title("Library AI Showcase")

    repo = configure_model_repository()

    image = upload_image()

    if image:
        ai_model_name = st.selectbox(
            "Select AI Model",
            repo.list_ai_models()
        )

        output_format = st.selectbox(
            "Select output format",
            repo.list_output_generators()
        )

        if st.button("Generate"):
            result = process_images(repo, [image], ai_model_name, output_format)
            st.text_area("Generated Output", result, height=300)


if __name__ == "__main__":
    main()