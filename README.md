# 💊 Farmacontable

**Farmacontable** es un sistema de contabilidad para farmacias desarrollado en Python con interfaz de escritorio (Tkinter) y base de datos PostgreSQL. Permite gestionar clientes, farmacias, productos, facturas, inventario y contabilidad general de forma local, sin necesidad de conexión a internet.

---

## 📦 Características

- Autenticación con login
- Gestión de usuarios con roles (`admin`, `vendedor`, etc.)
- Registro y consulta de clientes y farmacias
- Gestión de productos con stock e inventario
- Registro de facturas y control de ventas
- Interfaz gráfica intuitiva y modular
- Arquitectura por capas: GUI, controller, service, repository
- Conexión a PostgreSQL vía `psycopg2`
- Variables de entorno gestionadas con `.env`

---

## 🚀 Requisitos

- Python 3.11+
- PostgreSQL
- pipenv o venv
- Docker (opcional para pruebas)

---

## ⚙️ Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/tu-usuario/farmacontable.git
cd farmacontable
```

2.	Crea y activa un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3.	Instala dependencias:

```bash
pip install -r requirements.txt
```

4.	Crea un archivo .env con la variable de conexión a PostgreSQL:

```bash
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/farmacontable
```

⸻

## ▶️ Ejecución

```bash
python main.py
```

La interfaz se abrirá con las opciones de gestión habilitadas.

⸻

## 🗂️ Estructura del Proyecto

```bash
farmacontable/
│
├── db/                     # Repositorios y acceso a base de datos
│   └── connection.py       # Manejo de conexión
├── models/                 # Clases de dominio (Cliente, Usuario, etc.)
├── services/               # Lógica de negocio (login, CRUD, validaciones)
├── controllers/            # (opcional) Vínculo entre GUI y lógica (si aplica)
├── gui/                    # Formularios Tkinter (login, clientes, productos, etc.)
│
├── global_state.py         # Manejo de sesión activa
├── main.py                 # Punto de entrada (muestra login y lanza UI)
├── requirements.txt
├── .env                    # Variables de entorno (NO subir al repo)
├── .gitignore
└── README.md
```

⸻

## 🔐 Autenticación y Sesión

- Se requiere iniciar sesión para acceder al sistema.
- El rol del usuario se guarda en memoria y puede condicionar el acceso a ciertas funcionalidades.
- El sistema usa un archivo global_state.py para gestionar la sesión actual.

## 📌 Licencia

MIT License. Desarrollado por Gabriel Jaime Cardona.