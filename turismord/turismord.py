"""
TurismoRD – App principal Reflex
Monta las 3 páginas y la API REST
"""
import reflex as rx
from turismord.backend.database import init_db
from turismord.backend.api import api
from turismord.pages.inicio import index
from turismord.pages.descripcion import descripcion
from turismord.pages.reservas import reservas

# Initialize DB and seed data on startup
init_db()

# Reflex app
app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500&display=swap",
    ],
    style={
        "*": {"box_sizing": "border_box", "margin": "0", "padding": "0"},
        "body": {"font_family": "'DM Sans', system-ui, sans-serif"},
    },
)

# Pages
app.add_page(index, route="/", title="TurismoRD – Descubre la República Dominicana")
app.add_page(descripcion, route="/descripcion", title="Descripción del Tour – TurismoRD")
app.add_page(reservas, route="/reservas", title="Reservar Tour – TurismoRD")

# Mount FastAPI for API routes
app.api = api
