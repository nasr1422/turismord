# 🌴 TurismoRD – Plataforma de Reservas y Ofertas Turísticas

Aplicación web completa desarrollada en **Python con Reflex**, que permite explorar ofertas turísticas, ver descripciones detalladas y realizar reservas en línea.

---

## 🏗️ Estructura de Carpetas

```
turismord/
├── turismord/
│   ├── turismord.py          # App principal: registra páginas y monta la API
│   ├── state.py              # Estado global compartido
│   ├── pages/
│   │   ├── inicio.py         # Página de Inicio (/)
│   │   ├── descripcion.py    # Página de Descripción (/descripcion)
│   │   └── reservas.py       # Página de Reservas (/reservas)
│   ├── components/
│   │   └── shared.py         # Navbar, Footer y componentes reutilizables
│   └── backend/
│       ├── database.py       # SQLAlchemy: modelos Oferta y Reserva + seed
│       └── api.py            # API REST FastAPI montada en Reflex
├── assets/                   # Archivos estáticos (Reflex los sirve automáticamente)
├── rxconfig.py               # Configuración Reflex
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Cómo instalar y ejecutar

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/turismord.git
cd turismord
```

### 2. Crear entorno virtual e instalar dependencias
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 3. Configurar variables de entorno (opcional)
```bash
cp .env.example .env
# Para desarrollo local no se requiere nada: usa SQLite automáticamente.
# Para producción, editar DATABASE_URL con tu MySQL.
```

### 4. Ejecutar la aplicación
```bash
reflex run
```

La app estará disponible en: **http://localhost:3000**  
La API REST en: **http://localhost:3000/api/ofertas**  
Documentación de la API: **http://localhost:8000/docs**

---

## 🔌 Endpoints de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/ofertas` | Listar ofertas (`?busqueda=texto`) |
| `GET` | `/api/ofertas/{id}` | Detalle de una oferta |
| `POST` | `/api/reservas` | Registrar nueva reserva |
| `GET` | `/api/reservas` | Listado de reservas |
| `GET` | `/api/reservas/{id}` | Detalle de una reserva |

---

## 🌐 Despliegue en Render

1. Subir a GitHub con GitFlow (ramas: `main`, `develop`, `feature/*`)
2. En Render → New Web Service → conectar repositorio
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `reflex run --env prod`
5. Agregar variable `DATABASE_URL` apuntando a MySQL en la nube

---

## 🌿 GitFlow

```
main          → Producción
develop       → Integración
feature/ui    → Desarrollo UI con Reflex
feature/api   → Endpoints REST
release/v1.0  → Preparación de release
```

---

## 🛠️ Tecnologías

- **Reflex** – Framework Python full-stack (frontend + backend en Python puro)
- **FastAPI** – API REST montada dentro de Reflex
- **SQLAlchemy** – ORM para base de datos
- **SQLite** (dev) / **MySQL** (prod)
- **Pydantic** – Validación de datos

---

## 👥 Créditos

Proyecto Final – Desarrollo Web  
© 2025 TurismoRD
