"""
API REST endpoints – mounted into Reflex app
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from sqlalchemy.orm import Session

from turismord.backend.database import get_db, Oferta, Reserva, init_db

api = FastAPI(title="TurismoRD API", version="1.0.0")

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Schemas ────────────────────────────────────────────────────────────
class ReservaIn(BaseModel):
    oferta_id: int
    oferta_nombre: str
    nombre: str
    apellido: str
    email: str
    telefono: Optional[str] = None
    fecha_viaje: str
    personas: int = 1
    notas: Optional[str] = None
    metodo_pago: str = "tarjeta"
    total: float


# ── Ofertas ────────────────────────────────────────────────────────────
@api.get("/api/ofertas")
def listar_ofertas(busqueda: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Oferta).filter(Oferta.activa == True)
    if busqueda:
        t = f"%{busqueda}%"
        q = q.filter(Oferta.nombre.ilike(t) | Oferta.ubicacion.ilike(t))
    return q.all()


@api.get("/api/ofertas/{oferta_id}")
def obtener_oferta(oferta_id: int, db: Session = Depends(get_db)):
    o = db.query(Oferta).filter(Oferta.id == oferta_id).first()
    if not o:
        raise HTTPException(404, "Oferta no encontrada")
    return o


# ── Reservas ───────────────────────────────────────────────────────────
@api.post("/api/reservas", status_code=201)
def crear_reserva(data: ReservaIn, db: Session = Depends(get_db)):
    oferta = db.query(Oferta).filter(Oferta.id == data.oferta_id, Oferta.activa == True).first()
    if not oferta:
        raise HTTPException(404, "Oferta no disponible")
    total = round(oferta.precio * data.personas * 1.05, 2)
    r = Reserva(**data.dict(exclude={"total"}), total=total, estado="pendiente")
    db.add(r)
    db.commit()
    db.refresh(r)
    return {"id": r.id, "estado": r.estado, "total": r.total}


@api.get("/api/reservas")
def listar_reservas(db: Session = Depends(get_db)):
    return db.query(Reserva).order_by(Reserva.creado_en.desc()).all()


@api.get("/api/reservas/{reserva_id}")
def obtener_reserva(reserva_id: int, db: Session = Depends(get_db)):
    r = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not r:
        raise HTTPException(404, "Reserva no encontrada")
    return r
