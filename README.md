
# Sistema de Reclamos

## 📌 Nombre del sistema
**Sistema de Reclamos (sistemaReclamos)**

## 📝 Descripción breve
Aplicación web desarrollada en Django para la gestión de reclamos.  
Permite registrar reclamos, asignarlos a categorías y darles seguimiento según su estado y prioridad.  
Incluye roles diferenciados para administrador y operador.

## ⚙️ Tecnologías utilizadas
- Python 3.12
- Django 5.x
- Base de datos SQLite (por defecto) o PostgreSQL
- HTML, CSS y Bootstrap para la interfaz
- PythonAnywhere (plataforma de despliegue)

## 🚀 Cómo instalar el proyecto
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/usuario/sistema-reclamos.git
   cd sistema-reclamos


2-Crear y activar entorno virtual:


python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac

3-Instalar dependencias:

pip install -r requirements.txt

4-Aplicar migraciones:

python manage.py migrate


Cómo ejecutar el sistema

1-Levantar el servidor de desarrollo:

python manage.py runserver

2-Acceder en el navegador a:
http://127.0.0.1:8000/


3-Usuario administrador

python manage.py createsuperuser
	
Para crear un superusuario:

python manage.py createsuperuser


Funcionalidades principales
Registro y gestión de reclamos con categorías, estados y prioridades.

Roles diferenciados:

Administrador: gestiona usuarios, categorías y reclamos.

Operador: atiende reclamos asignados.

ABM (Alta, Baja, Modificación) de usuarios, reclamos y categorías.

Panel de administración de Django para gestión avanzada.

Interfaz web simple y práctica para registrar y consultar reclamos.






SOLO EN WINDOWS

## 🚀 Cómo instalar el proyecto

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/usuario/sistema-reclamos.git
   cd sistema-reclamos


2-Crear y activar entorno virtual:
python -m venv venv
venv\Scripts\activate

3-Instalar dependencias:
pip install -r requirements.txt

4-Aplicar migraciones:
python manage.py migrate


📌 En Linux/Mac la activación cambia a:
```bash
source venv/bin/activate


## ☁️ Despliegue en PythonAnywhere

1. **Crear cuenta** en [PythonAnywhere](https://www.pythonanywhere.com/).
2. **Subir el proyecto**:
   - Podés clonar tu repositorio desde GitHub:
     ```bash
     git clone https://github.com/usuario/sistema-reclamos.git
     ```
   - O subir los archivos manualmente.
3. **Crear un virtualenv** en PythonAnywhere:
   ```bash
   mkvirtualenv --python=python3.12 venv
   pip install -r requirements.txt

Configurar la aplicación web:

En el panel de PythonAnywhere, ir a Web → Add a new web app.

Elegir Manual configuration → Django → versión de Python.

Editar el archivo WSGI (/var/www/usuario_pythonanywhere_com_wsgi.py) para que apunte a tu proyecto:


import os, sys

path = '/home/usuario/sistema-reclamos'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'sistema_reclamos.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

5-Migrar la base de datos:

python manage.py migrate

6-Crear superusuario (si corresponde):
python manage.py createsuperuser

7-Reiniciar la aplicación web desde el panel de PythonAnywhere.


Reiniciar la aplicación web desde el panel de PythonAnywhere.














	



















