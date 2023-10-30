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

# Guía de Instalación y Conexión de XAMPP, MySQL y Django

Este README te guiará a través de los pasos para instalar XAMPP, MySQL y conectarlos con un proyecto de Django para levantar una página web localmente.

## Instalación de XAMPP

1. Descarga XAMPP desde el sitio web oficial: https://www.apachefriends.org/index.html
2. Ejecuta el instalador y sigue las instrucciones.
3. Durante la instalación, asegúrate de incluir los componentes necesarios, como Apache y MySQL.
4. Inicia el Panel de Control de XAMPP y asegúrate de que los servicios de Apache y MySQL estén en ejecución.

## Configuración de MySQL

1. Abre el Panel de Control de XAMPP.
2. Haz clic en el botón "Admin" para abrir phpMyAdmin en tu navegador.
3. Crea una nueva base de datos para tu proyecto Django.

## Configuración de un entorno virtual de Django

1. Asegúrate de tener Python instalado. Puedes verificarlo ejecutando `python --version` en la terminal.
2. Instala Django utilizando pip:
   ```
   pip install Django
   ```
3. Crea un entorno virtual para tu proyecto:
   ```
   python -m venv myenv
   ```
4. Activa el entorno virtual:
   - En Windows:
     ```
     myenv\Scripts\activate
     ```
   - En macOS y Linux:
     ```
     source myenv/bin/activate
     ```
5. Crea un nuevo proyecto de Django:
   ```
   django-admin startproject myproject
   ```
6. Abre el archivo `myproject/settings.py` y configura la base de datos para utilizar MySQL:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'nombre_de_tu_base_de_datos',
           'USER': 'tu_usuario_de_mysql',
           'PASSWORD': 'tu_contraseña_de_mysql',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

7. Asegúrate de que la aplicación esté conectada a la base de datos correctamente. Ejecuta las migraciones:

   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

8. Crea un superusuario para acceder al panel de administración de Django:

   ```
   python manage.py createsuperuser
   ```

## Creación y ejecución de la aplicación de Django

1. Crea una nueva aplicación en tu proyecto Django:

   ```
   python manage.py startapp myapp
   ```

2. Define las rutas, vistas y plantillas para tu aplicación.
3. Ejecuta el servidor de desarrollo:

   ```
   python manage.py runserver
   ```

4. Abre tu navegador y visita `http://localhost:8000` para ver tu página web local.

Ahora has instalado XAMPP, configurado MySQL y conectado tu proyecto de Django para levantar una página web local. ¡Disfruta desarrollando tu sitio web!

Asegúrate de reemplazar `"nombre_de_tu_base_de_datos"`, `"tu_usuario_de_mysql"`, y `"tu_contraseña_de_mysql"` con la información correcta de tu base de datos MySQL. Además, adapta los nombres de proyecto y aplicación según tus necesidades.
