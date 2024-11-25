# 🌐 Proyecto Django

Este es un proyecto Django diseñado para aplicar los conocimientos adquiridos en el bootcamp de la empresa Ecom, este pequeño sistema se trata de emular lo que son transacciones de dinero con cuentas dadas de alta en el sistema.

A continuación, se describen los pasos necesarios para levantar el proyecto en tu entorno local. 

Asegúrate de tener instalados los siguientes componentes: 
1. Python 3.10 o superior, 
2. pip
3. PostgreSQL 
4. Git
5. Virtualenv  

Para comenzar, sigue estos pasos: 

1. **Clona el repositorio** 

2. **Crea y activa un entorno virtual**: ```bash python3 -m venv venv source venv/bin/activate  # Linux/MacOS 
venv\Scripts\activate     # Windows ``` 

3. **Instala las dependencias** del proyecto: 
```bash pip install -r ./requirements/requirements.txt ``` 

4. **Configura la base de datos**: 
- Asegúrate de que el servidor de base de datos esté en funcionamiento. 
- Crea una base de datos para el proyecto. Por ejemplo, en PostgreSQL: 
```CREATE DATABASE nombre_base_datos; ``` 

- Crea el archivo `.env` con los detalles de la conexión a la base de datos: 
```#ENTORNO
ENVIROMENT_RUN=
SECRET_KEY=
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=

#database
POSTGRES_HOST=
POSTGRES_PORT=
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD= 
``` 

5. **Aplica las migraciones** para configurar la base de datos: 
- ```bash python manage.py makemigrations usuarios``` 
- ```bash python manage.py makemigrations transacciones``` 
- ```bash python manage.py migrate ``` 

6. **Crea un superusuario** para acceder al panel de administración de Django: 
- ```bash python manage.py createsuperuser ```

7. **Inicia el servidor de desarrollo**: ```bash python manage.py runserver ``` 

8. **Accede al proyecto**: 
- Abre tu navegador y ve a [http://127.0.0.1:8000](http://127.0.0.1:8000) para ver la aplicación en funcionamiento. 
- Si necesitas acceder al panel de administración, ve a [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) e ingresa con el superusuario creado. 

