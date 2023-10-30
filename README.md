# 04-not-scrum-master-team

* [Wiki](https://github.com/INF225-2023-2-P201/04-not-scrum-master-team/wiki)


# Instalación de spaCy

Este tutorial te guiará a través del proceso de instalación de la librería spaCy en tu sistema. spaCy es una poderosa librería de procesamiento de lenguaje natural (NLP) que te permitirá realizar tareas de procesamiento de texto de manera eficiente.

## Prerrequisitos

Antes de comenzar con la instalación de spaCy, asegúrate de tener instalado Python en tu sistema. Puedes descargar Python desde [python.org](https://www.python.org/downloads/) e instalarlo siguiendo las instrucciones adecuadas para tu sistema operativo.

## Pasos para la instalación

Sigue estos pasos para instalar spaCy en tu entorno de desarrollo:

1. **Creación de un entorno virtual (opcional pero recomendado):** Se recomienda crear un entorno virtual para mantener las dependencias del proyecto aisladas de otras instalaciones de Python. Utiliza el siguiente comando para crear un entorno virtual:

   ```bash
   python -m venv myenv
   ```

   Donde `myenv` es el nombre que desees darle a tu entorno virtual.

2. **Activación del entorno virtual (opcional):** Si has creado un entorno virtual en el paso anterior, actívalo usando el comando adecuado para tu sistema operativo:

   - En Windows:

     ```bash
     myenv\Scripts\activate
     ```

   - En macOS y Linux:

     ```bash
     source myenv/bin/activate
     ```

3. **Instalación de spaCy:** Ahora puedes instalar spaCy usando pip. Ejecuta el siguiente comando:

   ```bash
   pip install spacy
   ```

4. **Descarga de modelos de idioma (opcional pero recomendado):** spaCy proporciona modelos preentrenados para varios idiomas. Puedes descargar un modelo de idioma utilizando el siguiente comando, reemplazando `idioma` con el idioma que necesites (por ejemplo, `es` para español):

   ```bash
   python -m spacy download idioma
   ```

   Por ejemplo, para descargar el modelo de idioma español (que es el necesario para el buen uso del software), ejecuta:

   ```bash
   python -m spacy download es
   ```

## Verificación de la instalación

Para verificar que spaCy se ha instalado correctamente, puedes ejecutar el código fuente.
