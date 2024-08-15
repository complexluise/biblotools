# Extracción Automática de Información de Libros desde Imágenes

¡Bienvenido a nuestro proyecto de extracción automática de información de libros a partir de imágenes! Este script utiliza la API de Anthropic para analizar imágenes de portadas de libros y extraer datos relevantes, incluyendo el ISBN, en formato JSON.

## Características

- **Conversión de imágenes a Base64**: El script convierte imágenes en su representación en Base64 para su procesamiento.
- **Generación de prompts personalizados**: Se crea un mensaje específico para el modelo de IA con las imágenes y un prompt definido.
- **Extracción automática**: Utiliza el modelo de lenguaje Claude 3.5 de Anthropic para extraer información relevante de las imágenes proporcionadas.
- **Exportación de resultados**: Los datos extraídos se guardan en un archivo CSV para su uso posterior.

## Requisitos

- Python 3.x
- Paquetes de Python: `base64`, `os`, `csv`, `click`, `anthropic`
- Una clave API válida de Anthropic

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/tu_usuario/proyecto-extraccion-libros.git
    cd proyecto-extraccion-libros
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

Este script se ejecuta desde la línea de comandos y requiere como argumento la carpeta que contiene las imágenes de los libros.

```bash
python extract_books.py /ruta/a/carpeta/de/imagenes --output_csv resultado.csv
```

- `image_folder`: Ruta a la carpeta que contiene las imágenes de los libros.
- `--output_csv`: (Opcional) Nombre del archivo CSV donde se almacenará la información extraída. Por defecto es `output.csv`.

## Ejemplo de Ejecución

```bash
python extract_books.py ./imagenes_libros --output_csv libros_extraidos.csv
```

## Estructura del Proyecto

- `extract_books.py`: Script principal que realiza la extracción de información.
- `requirements.txt`: Lista de dependencias necesarias para el proyecto.
- `README.md`: Este archivo, que explica cómo usar el proyecto.

## Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar este proyecto, no dudes en enviar un pull request o abrir un issue.

## Licencia

Este proyecto está bajo la Licencia MIT. ¡Siéntete libre de usarlo y modificarlo como desees!

---

¡Gracias por usar este proyecto! Esperamos que te sea útil y facilite tu trabajo con la extracción de datos de libros a partir de imágenes. 🚀📚