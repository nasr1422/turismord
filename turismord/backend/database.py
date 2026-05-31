"""
Database configuration - SQLAlchemy + MySQL Aiven
"""
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from dotenv import load_dotenv
import enum

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./turismord.db"
)

# SSL config for Aiven MySQL
if "aivencloud" in DATABASE_URL:
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ca_path = os.path.join(base_dir, "ca.pem")
    connect_args = {"ssl": {"ca": ca_path}}
elif "sqlite" in DATABASE_URL:
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Oferta(Base):
    __tablename__ = "ofertas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    ubicacion = Column(String(150), nullable=False)
    descripcion_corta = Column(String(400), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Float, nullable=False)
    duracion = Column(String(50), nullable=False)
    dificultad = Column(String(50), default="Facil")
    idioma = Column(String(100), default="Espanol / Ingles")
    incluye = Column(String(300), nullable=True)
    grupo_max = Column(String(50), default="20 personas")
    descuento = Column(Integer, nullable=True)
    imagen = Column(String(500), nullable=True)
    activa = Column(Boolean, default=True)
    creado_en = Column(DateTime, server_default=func.now())


class Reserva(Base):
    __tablename__ = "reservas"
    id = Column(Integer, primary_key=True, index=True)
    oferta_id = Column(Integer, nullable=False)
    oferta_nombre = Column(String(200), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False)
    telefono = Column(String(30), nullable=True)
    fecha_viaje = Column(String(20), nullable=False)
    personas = Column(Integer, nullable=False, default=1)
    notas = Column(Text, nullable=True)
    metodo_pago = Column(String(30), default="tarjeta")
    total = Column(Float, nullable=False)
    estado = Column(String(20), default="pendiente")
    creado_en = Column(DateTime, server_default=func.now())


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create tables and seed demo data."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(Oferta).count() == 0:
        seed_offers = [
            Oferta(nombre="Cataratas del Limon & Samana", ubicacion="Samana, RD",
                   descripcion_corta="Descubre la impresionante cascada El Limon rodeada de naturaleza tropical.",
                   descripcion="Un tour completo que combina la majestuosa cascada El Limon con un paseo en yola por la bahia de Samana. Incluye almuerzo tipico dominicano.",
                   precio=89, duracion="1 dia", dificultad="Moderada", descuento=15,
                   incluye="Guia, transporte A/R, almuerzo, seguro", grupo_max="15 personas",
                   imagen="https://images.unsplash.com/photo-1586611292717-f828b167408c?w=800&q=80"),
            Oferta(nombre="Isla Saona - Paraiso Natural", ubicacion="La Romana, RD",
                   descripcion_corta="Navega hacia la famosa Isla Saona con aguas turquesas y estrellas de mar.",
                   descripcion="Embarquese en un catamaran de lujo hacia la Isla Saona. Nada con estrellas de mar y almuerza en la playa.",
                   precio=75, duracion="1 dia", dificultad="Facil", descuento=None,
                   incluye="Catamaran, almuerzo buffet, bebidas, guia", grupo_max="40 personas",
                   imagen="https://images.unsplash.com/photo-1559128010-7c1ad6e1b6a5?w=800&q=80"),
            Oferta(nombre="Ciudad Colonial & Gastronomia", ubicacion="Santo Domingo, RD",
                   descripcion_corta="Recorre el primer asentamiento europeo del Nuevo Mundo.",
                   descripcion="Recorrido a pie por la Zona Colonial, Patrimonio UNESCO. Finaliza con una clase de cocina criolla.",
                   precio=55, duracion="Medio dia", dificultad="Facil", descuento=None,
                   incluye="Guia certificado, degustaciones, materiales", grupo_max="12 personas",
                   imagen="https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&q=80"),
            Oferta(nombre="Punta Cana All-Inclusive", ubicacion="Punta Cana, RD",
                   descripcion_corta="Experiencia completa en las mejores playas del Caribe.",
                   descripcion="3 dias y 2 noches en resort 5 estrellas. Incluye todas las comidas y bebidas ilimitadas.",
                   precio=149, duracion="3 dias", dificultad="Facil", descuento=20,
                   incluye="Hotel 5 estrellas, comidas, bebidas, deportes acuaticos", grupo_max="Sin limite",
                   imagen="https://images.unsplash.com/photo-1530789253388-582c481c54b0?w=800&q=80"),
            Oferta(nombre="Jarabacoa Adventure - Rafting", ubicacion="Jarabacoa, RD",
                   descripcion_corta="Adrenalina pura en el rio Yaque del Norte con rafting y canopy.",
                   descripcion="Un dia de aventura con rafting grado III-IV, canopy de 200m y senderismo hasta el Salto Jimenoa.",
                   precio=95, duracion="1 dia", dificultad="Alta", descuento=None,
                   incluye="Equipo, guia, almuerzo, seguro aventura", grupo_max="12 personas",
                   imagen="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80"),
            Oferta(nombre="Los Haitises & Manglares", ubicacion="Samana, RD",
                   descripcion_corta="Navega por el parque nacional Los Haitises y sus cuevas tainas.",
                   descripcion="Explora el Parque Nacional Los Haitises. Visita cuevas con arte rupestre taino e islotes de manglar.",
                   precio=85, duracion="1 dia", dificultad="Moderada", descuento=10,
                   incluye="Lancha, guia naturalista, snorkel, almuerzo", grupo_max="20 personas",
                   imagen="https://images.unsplash.com/photo-1518623489648-a173ef7824f3?w=800&q=80"),
        ]
        db.add_all(seed_offers)
        db.commit()
        print(f"Base de datos inicializada con {len(seed_offers)} ofertas.")
    db.close()
