
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
	



















