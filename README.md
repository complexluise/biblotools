# Extracción Automática de Información de Libros desde Imágenes

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://libroscan.streamlit.app)

Esta aplicación Streamlit utiliza la API de Anthropic para analizar imágenes de portadas de libros y extraer datos relevantes, incluyendo el ISBN, presentándolos en una tabla interactiva.

## Características

- **Interfaz web intuitiva**: Utiliza Streamlit para proporcionar una experiencia de usuario amigable.
- **Extracción automática**: Emplea el modelo de lenguaje Claude 3.5 de Anthropic para extraer información relevante de las imágenes proporcionadas.
- **Visualización de resultados**: Los datos extraídos se muestran en una tabla interactiva dentro de la aplicación.

## Requisitos

- Python 3.x
- Paquetes de Python: `streamlit`, `pillow`, `pandas`, `anthropic`
- Una clave API válida de Anthropic

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/complexluise/foto_a_formato_bibliotecario.git
    cd foto_a_formato_bibliotecario
    ```

2. Instala las dependencias necesarias:
    ```bash
    pip install -r requirements.txt
    ```

3. Configura tu clave API de Anthropic como una variable de entorno:
    ```bash
    export ANTHROPIC_KEY="tu_clave_api"
    ```

## Uso

Para ejecutar la aplicación Streamlit:

    ```bash
    streamlit run app/main.py
    ```

Luego, abre tu navegador y ve a la dirección que se muestra en la consola (generalmente http://localhost:8501).

## Cómo usar la aplicación
Carga las imágenes de los libros utilizando el botón de carga de archivos.
Selecciona el modelo de IA que deseas utilizar. (Por el momento solo esta Anthropic - Claude Sonnet 3.5)
Elige el formato de salida deseado.
Haz clic en "Generar" para procesar las imágenes y ver los resultados.


## Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar este proyecto, no dudes en enviar un pull request o abrir un issue.

## Licencia

Este proyecto está bajo la Licencia GNU GENERAL PUBLIC LICENSE. ¡Siéntete libre de usarlo y modificarlo como desees!

¡Gracias por usar este proyecto! Esperamos que te sea útil y facilite tu trabajo con la extracción de datos de libros a partir de imágenes. 🚀📚
