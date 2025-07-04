# 💊 Farmacontable

**Farmacontable** es un sistema de contabilidad para farmacias desarrollado en Python con interfaz de escritorio (Tkinter) y base de datos PostgreSQL. Permite gestionar clientes, farmacias, productos, facturas, inventario y contabilidad general de forma local, sin necesidad de conexión a internet.

---

## 📦 Características

- Registro y consulta de clientes y farmacias
- Gestión de productos con stock e inventario
- Interfaz gráfica intuitiva
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
├── db/                 # Conexión y queries SQL
├── models/             # Clases de dominio (Cliente, Farmacia, Producto...)
├── services/           # Lógica de negocio
├── controllers/        # Enlace entre GUI y lógica
├── gui/                # Formularios Tkinter
├── main.py             # Punto de entrada
├── .env                # Variables de entorno (NO subir al repo)
├── .gitignore
└── README.md
```

⸻

## 📌 Licencia

MIT License. Desarrollado por Gabriel Jaime Cardona.