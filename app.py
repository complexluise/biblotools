import streamlit as st
from PIL import Image
import pandas as pd
from biblotools.use_cases import configure_model_repository, process_images


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode("utf-8")

def upload_images():
    uploaded_files = st.file_uploader("Choose image files", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    images = []
    if uploaded_files:
        col1, col2 = st.columns(2)
        for i, uploaded_file in enumerate(uploaded_files):
            image = Image.open(uploaded_file)
            images.append(image)

        with col1:
            st.image(images[0], caption=f"Uploaded Image: {uploaded_file.name}", width=300)
        with col2:
            st.image(images[1], caption=f"Uploaded Image: {uploaded_file.name}", width=300)
    return images


def main():
    st.title("Fotos de libro a tabla")

    repo = configure_model_repository()

    images = upload_images()

    if images:
        ai_model_name = st.selectbox(
            "Selecciona el modelo de IA",
            repo.list_ai_models()
        )

        output_format = st.selectbox(
            "Selecciona el formato de salida",
            repo.list_output_generators()
        )

        if st.button("Generar"):
            df = process_images(repo, images, ai_model_name, output_format)

            # Assuming results is a list of dictionaries
            # TODO depending on the OutputGenerator, this might need to be a different data structure
            st.table(df)
            st.download_button(
                label="Descargar tabla como CSV",
                data=convert_df(df),
                file_name="tabla_libros.csv",
                mime="text/csv",
            )


if __name__ == "__main__":
    main()
