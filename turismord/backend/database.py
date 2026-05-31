"""
Database configuration – SQLAlchemy + MySQL (o SQLite para dev)
"""
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, Boolean, Enum as SAEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import enum

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./turismord.db"   # SQLite for local dev; switch to MySQL in prod
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class EstadoReserva(str, enum.Enum):
    pendiente = "pendiente"
    confirmada = "confirmada"
    cancelada = "cancelada"


class Oferta(Base):
    __tablename__ = "ofertas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    ubicacion = Column(String(150), nullable=False)
    descripcion_corta = Column(String(400), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Float, nullable=False)
    duracion = Column(String(50), nullable=False)
    dificultad = Column(String(50), default="Fácil")
    idioma = Column(String(100), default="Español / Inglés")
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
            Oferta(nombre="Cataratas del Limón & Samaná", ubicacion="Samaná, RD",
                   descripcion_corta="Descubre la impresionante cascada El Limón rodeada de naturaleza tropical y relájate en las playas de Samaná.",
                   descripcion="Un tour completo que combina la majestuosa cascada El Limón de 52 metros con un paseo en yola por la bahía de Samaná. Incluye almuerzo típico dominicano y tiempo libre en la playa.",
                   precio=89, duracion="1 día", dificultad="Moderada", descuento=15,
                   incluye="Guía, transporte A/R, almuerzo, seguro", grupo_max="15 personas",
                   imagen="https://images.unsplash.com/photo-1586611292717-f828b167408c?w=800&q=80"),
            Oferta(nombre="Isla Saona – Paraíso Natural", ubicacion="La Romana, RD",
                   descripcion_corta="Navega hacia la famosa Isla Saona con sus aguas turquesas y bancos de estrellas de mar en una piscina natural única.",
                   descripcion="Embárcate en un catamarán de lujo hacia la Isla Saona, paraíso natural declarado parque nacional. Nada con estrellas de mar, almuerza en la playa y regresa en lancha rápida.",
                   precio=75, duracion="1 día", dificultad="Fácil", descuento=None,
                   incluye="Catamarán, almuerzo buffet, bebidas, guía", grupo_max="40 personas",
                   imagen="https://images.unsplash.com/photo-1559128010-7c1ad6e1b6a5?w=800&q=80"),
            Oferta(nombre="Ciudad Colonial & Gastronomía", ubicacion="Santo Domingo, RD",
                   descripcion_corta="Recorre el primer asentamiento europeo del Nuevo Mundo y descubre la rica gastronomía dominicana con un chef local.",
                   descripcion="Recorrido a pie por la Zona Colonial, Patrimonio UNESCO. Visita el Alcázar de Colón, la Catedral Primada y finaliza con una clase de cocina criolla con productos del mercado local.",
                   precio=55, duracion="Medio día", dificultad="Fácil", descuento=None,
                   incluye="Guía certificado, degustaciones, materiales", grupo_max="12 personas",
                   imagen="https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&q=80"),
            Oferta(nombre="Punta Cana All-Inclusive", ubicacion="Punta Cana, RD",
                   descripcion_corta="Experiencia completa en las mejores playas del Caribe con actividades acuáticas, deportes y entretenimiento sin límites.",
                   descripcion="3 días y 2 noches en resort 5 estrellas en Punta Cana. Incluye todas las comidas, bebidas ilimitadas, deportes acuáticos, snorkel, kayak y entretenimiento nocturno.",
                   precio=149, duracion="3 días", dificultad="Fácil", descuento=20,
                   incluye="Hotel 5★, comidas, bebidas, deportes acuáticos", grupo_max="Sin límite",
                   imagen="https://images.unsplash.com/photo-1530789253388-582c481c54b0?w=800&q=80"),
            Oferta(nombre="Jarabacoa Adventure – Rafting", ubicacion="Jarabacoa, RD",
                   descripcion_corta="Adrenalina pura en el río Yaque del Norte con rafting, canopy y senderismo en la Cordillera Central.",
                   descripcion="Un día lleno de aventura en la 'Ciudad de las Flores'. Rafting grado III-IV, canopy de 200m sobre el bosque y senderismo hasta el Salto Jimenoa. Almuerzo campestre incluido.",
                   precio=95, duracion="1 día", dificultad="Alta", descuento=None,
                   incluye="Equipo, guía, almuerzo, seguro aventura", grupo_max="12 personas",
                   imagen="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80"),
            Oferta(nombre="Los Haitises & Manglares", ubicacion="Samaná, RD",
                   descripcion_corta="Navega por el parque nacional Los Haitises, cuevas con pictografías taínas y el ecosistema de manglar más denso del Caribe.",
                   descripcion="Explora el Parque Nacional Los Haitises en lancha. Visita cuevas con arte rupestre taíno, islotes de manglar con aves endémicas y el estero Portillo.",
                   precio=85, duracion="1 día", dificultad="Moderada", descuento=10,
                   incluye="Lancha, guía naturalista, snorkel, almuerzo", grupo_max="20 personas",
                   imagen="https://images.unsplash.com/photo-1518623489648-a173ef7824f3?w=800&q=80"),
        ]
        db.add_all(seed_offers)
        db.commit()
    db.close()
