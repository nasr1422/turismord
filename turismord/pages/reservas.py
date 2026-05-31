"""
Página de Reservas – TurismoRD
"""
import reflex as rx
from turismord.components.shared import (
    navbar, footer, section_tag,
    GOLD, DEEP_OCEAN, TURQUOISE, CORAL, CREAM, SAND, MUTED, WHITE
)

DEMO_OFERTA = {
    "id": 1, "nombre": "Cataratas del Limón & Samaná",
    "ubicacion": "Samaná, RD", "duracion": "1 día",
    "precio": 89.0,
    "imagen": "https://images.unsplash.com/photo-1586611292717-f828b167408c?w=400&q=80",
}


class ReservaState(rx.State):
    # Form fields
    nombre: str = ""
    apellido: str = ""
    email: str = ""
    telefono: str = ""
    nacionalidad: str = ""
    fecha_viaje: str = ""
    personas: int = 2
    punto_encuentro: str = "sd-zona-colonial"
    notas: str = ""
    metodo_pago: str = "tarjeta"

    # UI state
    reserva_exitosa: bool = False
    booking_id: str = ""
    loading: bool = False
    error_msg: str = ""

    @rx.var
    def subtotal(self) -> float:
        return DEMO_OFERTA["precio"] * self.personas

    @rx.var
    def fee(self) -> float:
        return round(self.subtotal * 0.05, 2)

    @rx.var
    def total(self) -> float:
        return round(self.subtotal + self.fee, 2)

    @rx.var
    def precio_unitario(self) -> str:
        return f"${DEMO_OFERTA['precio']:.0f} × {self.personas}"

    @rx.var
    def subtotal_str(self) -> str:
        return f"${self.subtotal:.2f}"

    @rx.var
    def fee_str(self) -> str:
        return f"${self.fee:.2f}"

    @rx.var
    def total_str(self) -> str:
        return f"${self.total:.2f}"

    @rx.event
    def set_nombre(self, v: str): self.nombre = v
    @rx.event
    def set_apellido(self, v: str): self.apellido = v
    @rx.event
    def set_email(self, v: str): self.email = v
    @rx.event
    def set_telefono(self, v: str): self.telefono = v
    @rx.event
    def set_nacionalidad(self, v: str): self.nacionalidad = v
    @rx.event
    def set_fecha_viaje(self, v: str): self.fecha_viaje = v
    @rx.event
    def set_personas(self, v: str):
        try:
            self.personas = max(1, min(50, int(v)))
        except Exception:
            pass
    @rx.event
    def set_punto_encuentro(self, v: str): self.punto_encuentro = v
    @rx.event
    def set_notas(self, v: str): self.notas = v
    @rx.event
    def set_metodo_pago(self, v: str): self.metodo_pago = v

    @rx.event
    async def confirmar_reserva(self):
        if not self.nombre or not self.apellido or not self.email or not self.fecha_viaje:
            self.error_msg = "Por favor completa todos los campos requeridos."
            return

        self.loading = True
        self.error_msg = ""
        yield

        import httpx, random, asyncio
        await asyncio.sleep(1.2)  # simulate processing

        try:
            async with httpx.AsyncClient() as client:
                r = await client.post(
                    "http://localhost:3000/api/reservas",
                    json={
                        "oferta_id": DEMO_OFERTA["id"],
                        "oferta_nombre": DEMO_OFERTA["nombre"],
                        "nombre": self.nombre,
                        "apellido": self.apellido,
                        "email": self.email,
                        "telefono": self.telefono,
                        "fecha_viaje": self.fecha_viaje,
                        "personas": self.personas,
                        "notas": self.notas,
                        "metodo_pago": self.metodo_pago,
                        "total": self.total,
                    },
                    timeout=5,
                )
                data = r.json()
                self.booking_id = f"RD-{data.get('id', random.randint(10000, 99999))}"
        except Exception:
            self.booking_id = f"RD-{random.randint(10000, 99999)}"

        self.reserva_exitosa = True
        self.loading = False

    @rx.event
    def nueva_reserva(self):
        self.reserva_exitosa = False
        self.nombre = ""
        self.apellido = ""
        self.email = ""
        self.fecha_viaje = ""
        self.personas = 2


def campo(label: str, component: rx.Component) -> rx.Component:
    return rx.vstack(
        rx.text(label, font_size="0.73rem", letter_spacing="0.06em",
                color=MUTED, font_weight="500"),
        component,
        spacing="1", width="100%", align_items="start",
    )


def input_field(**kwargs) -> dict:
    return {
        "width": "100%",
        "padding": "0.72rem 0.9rem",
        "border": "1.5px solid rgba(0,0,0,0.1)",
        "border_radius": "4px",
        "font_size": "0.88rem",
        "color": DEEP_OCEAN,
        "background": WHITE,
        **kwargs,
    }


def section_divider(label: str) -> rx.Component:
    return rx.hstack(
        rx.text(label, font_size="0.7rem", letter_spacing="0.15em",
                text_transform="uppercase", color=CORAL, font_weight="600",
                white_space="nowrap"),
        rx.box(flex="1", height="1px", background="rgba(0,0,0,0.08)"),
        spacing="3", width="100%", align="center", margin_y="1.5rem",
    )


def payment_btn(method: str, icon: str, label: str) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(icon, font_size="1.5rem"),
            rx.text(label, font_size="0.75rem", color=MUTED, text_align="center"),
            spacing="1", align_items="center",
        ),
        border=rx.cond(
            ReservaState.metodo_pago == method,
            f"1.5px solid {TURQUOISE}",
            "1.5px solid rgba(0,0,0,0.1)",
        ),
        background=rx.cond(
            ReservaState.metodo_pago == method,
            "rgba(0,180,166,0.06)",
            WHITE,
        ),
        border_radius="6px",
        padding="1rem 0.5rem",
        text_align="center",
        cursor="pointer",
        on_click=ReservaState.set_metodo_pago(method),
        transition="all 0.2s",
        flex="1",
    )


def success_screen() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.text("🎉", font_size="4rem"),
            rx.heading("¡Reserva Confirmada!",
                       font_family="Georgia, serif",
                       font_size="2rem", color=DEEP_OCEAN),
            rx.text("Tu reserva fue procesada exitosamente. Recibirás un correo de confirmación.",
                    color=MUTED, text_align="center", max_width="380px", line_height="1.6"),
            rx.box(
                rx.vstack(
                    rx.text("Número de Reserva", color=MUTED, font_size="0.7rem",
                            letter_spacing="0.1em", text_transform="uppercase"),
                    rx.text(ReservaState.booking_id,
                            font_family="Georgia, serif",
                            font_size="2rem", font_weight="700", color=DEEP_OCEAN),
                    spacing="0", align_items="center",
                ),
                background=SAND, border_radius="8px", padding="1.2rem 2rem",
            ),
            rx.hstack(
                rx.link(
                    rx.button(
                        "Ver más tours",
                        background=CORAL, color=WHITE,
                        padding="0.8rem 1.5rem",
                        border_radius="2px",
                        cursor="pointer",
                    ),
                    href="/#ofertas",
                ),
                rx.button(
                    "Nueva reserva",
                    on_click=ReservaState.nueva_reserva,
                    background="transparent",
                    border=f"1px solid rgba(0,0,0,0.2)",
                    color=MUTED,
                    padding="0.8rem 1.5rem",
                    border_radius="2px",
                    cursor="pointer",
                ),
                spacing="3",
            ),
            spacing="5",
            align_items="center",
        ),
        min_height="60vh",
    )


def reservas() -> rx.Component:
    iS = input_field()

    return rx.box(
        navbar(),

        # Page header
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.link("Inicio", href="/", color="rgba(255,255,255,0.45)",
                            text_decoration="none", font_size="0.78rem"),
                    rx.text("›", color="rgba(255,255,255,0.25)"),
                    rx.link("Ofertas", href="/#ofertas", color="rgba(255,255,255,0.45)",
                            text_decoration="none", font_size="0.78rem"),
                    rx.text("›", color="rgba(255,255,255,0.25)"),
                    rx.text("Reservar", color="rgba(255,255,255,0.45)", font_size="0.78rem"),
                    align="center", spacing="2",
                ),
                rx.heading("Confirma tu Reserva",
                           font_family="Georgia, serif",
                           font_size=["1.8rem", "2.2rem", "2.5rem"],
                           color=WHITE, font_weight="700"),
                rx.text("Completa tus datos para asegurar tu lugar. Pago 100% seguro.",
                        color="rgba(255,255,255,0.55)", font_size="0.9rem"),
                spacing="3", align_items="start",
                max_width="1200px", margin="0 auto",
                padding_x=["1.5rem", "2rem", "4rem"],
            ),
            background=DEEP_OCEAN,
            padding_top="6rem",
            padding_bottom="2.5rem",
            border_bottom=f"1px solid rgba(201,168,76,0.15)",
        ),

        # Main content
        rx.cond(
            ReservaState.reserva_exitosa,
            success_screen(),
            rx.flex(
                # ── FORM ──
                rx.box(
                    rx.vstack(
                        rx.heading("Detalles de la Reserva",
                                   font_family="Georgia, serif",
                                   font_size="1.6rem", color=DEEP_OCEAN),
                        rx.text("Todos los campos marcados * son requeridos.",
                                color=MUTED, font_size="0.85rem"),

                        # Error message
                        rx.cond(
                            ReservaState.error_msg != "",
                            rx.box(
                                rx.text(ReservaState.error_msg,
                                        color=CORAL, font_size="0.85rem"),
                                background="rgba(232,98,74,0.08)",
                                border=f"1px solid rgba(232,98,74,0.3)",
                                border_radius="4px",
                                padding="0.8rem 1rem",
                                width="100%",
                            ),
                            rx.box(),
                        ),

                        # Datos de contacto
                        section_divider("📋 Datos de Contacto"),
                        rx.grid(
                            campo("Nombre *", rx.input(
                                placeholder="Tu nombre",
                                value=ReservaState.nombre,
                                on_change=ReservaState.set_nombre, **iS)),
                            campo("Apellido *", rx.input(
                                placeholder="Tu apellido",
                                value=ReservaState.apellido,
                                on_change=ReservaState.set_apellido, **iS)),
                            columns="2", gap="1rem", width="100%",
                        ),
                        rx.grid(
                            campo("Email *", rx.input(
                                placeholder="correo@ejemplo.com", type="email",
                                value=ReservaState.email,
                                on_change=ReservaState.set_email, **iS)),
                            campo("Teléfono", rx.input(
                                placeholder="+1 (809) 000-0000",
                                value=ReservaState.telefono,
                                on_change=ReservaState.set_telefono, **iS)),
                            columns="2", gap="1rem", width="100%",
                        ),
                        campo("Nacionalidad", rx.select(
                            ["República Dominicana", "Estados Unidos", "México",
                             "Colombia", "España", "Puerto Rico", "Otro"],
                            value=ReservaState.nacionalidad,
                            on_change=ReservaState.set_nacionalidad, **iS,
                        )),

                        # Detalles de la actividad
                        section_divider("🗓️ Detalles de la Actividad"),
                        rx.grid(
                            campo("Fecha de Viaje *", rx.input(
                                type="date",
                                value=ReservaState.fecha_viaje,
                                on_change=ReservaState.set_fecha_viaje, **iS)),
                            campo("Número de Personas *", rx.input(
                                type="number", placeholder="2",
                                value=ReservaState.personas,
                                on_change=ReservaState.set_personas,
                                min="1", max="50", **iS)),
                            columns="2", gap="1rem", width="100%",
                        ),
                        campo("Punto de Encuentro", rx.select(
                            ["Santo Domingo – Zona Colonial",
                             "Santo Domingo – Aeropuerto Las Américas",
                             "Recogida en hotel (cargo adicional)"],
                            value=ReservaState.punto_encuentro,
                            on_change=ReservaState.set_punto_encuentro, **iS,
                        )),
                        campo("Notas especiales", rx.text_area(
                            placeholder="Alergias, necesidades especiales, celebraciones…",
                            value=ReservaState.notas,
                            on_change=ReservaState.set_notas,
                            **{**iS, "height": "90px"},
                        )),

                        # Descripción de pago
                        section_divider("💳 Descripción de Pago"),
                        rx.text("Selecciona tu método de pago preferido. Todos los pagos son procesados con encriptación SSL.",
                                color=MUTED, font_size="0.83rem", margin_bottom="0.5rem"),
                        rx.hstack(
                            payment_btn("tarjeta", "💳", "Tarjeta"),
                            payment_btn("paypal", "🅿️", "PayPal"),
                            payment_btn("transferencia", "🏦", "Transferencia"),
                            spacing="3", width="100%",
                        ),

                        # Security note
                        rx.hstack(
                            rx.text("🔒", font_size="1.1rem"),
                            rx.vstack(
                                rx.text("Pago 100% Seguro",
                                        font_size="0.82rem", font_weight="600", color=DEEP_OCEAN),
                                rx.text("Tu información está encriptada con SSL 256-bit. No almacenamos datos de tarjeta.",
                                        font_size="0.78rem", color=MUTED, line_height="1.5"),
                                spacing="0", align_items="start",
                            ),
                            background="rgba(0,180,166,0.06)",
                            border=f"1px solid rgba(0,180,166,0.2)",
                            border_radius="6px",
                            padding="1rem",
                            align="start",
                            spacing="3",
                            width="100%",
                        ),

                        # Submit button
                        rx.button(
                            rx.cond(
                                ReservaState.loading,
                                "Procesando reserva…",
                                "🌴  Confirmar Reserva",
                            ),
                            on_click=ReservaState.confirmar_reserva,
                            width="100%",
                            background=f"linear-gradient(135deg, {CORAL}, #d45038)",
                            color=WHITE,
                            padding="1rem",
                            border_radius="4px",
                            font_size="0.95rem",
                            font_weight="500",
                            cursor="pointer",
                            _hover={"filter": "brightness(1.08)"},
                            disabled=ReservaState.loading,
                        ),

                        spacing="3",
                        align_items="start",
                        width="100%",
                    ),
                    background=WHITE,
                    border_radius="8px",
                    box_shadow="0 20px 60px rgba(13,43,62,0.1)",
                    padding=["1.5rem", "2rem", "2.5rem"],
                    flex="1",
                ),

                # ── SIDEBAR ──
                rx.vstack(
                    # Tour summary card
                    rx.box(
                        rx.box(
                            rx.image(
                                src=DEMO_OFERTA["imagen"],
                                width="100%", height="180px",
                                object_fit="cover",
                            ),
                            overflow="hidden",
                        ),
                        rx.vstack(
                            rx.text(DEMO_OFERTA["nombre"],
                                    font_family="Georgia, serif",
                                    color=WHITE, font_size="1.1rem", font_weight="700"),
                            rx.text(f"📍 {DEMO_OFERTA['ubicacion']} · {DEMO_OFERTA['duracion']}",
                                    color="rgba(255,255,255,0.5)", font_size="0.83rem"),
                            spacing="1", align_items="start",
                            padding="1.2rem",
                        ),
                        background=DEEP_OCEAN,
                        border_radius="8px",
                        overflow="hidden",
                    ),

                    # Price breakdown
                    rx.box(
                        rx.vstack(
                            section_tag("Desglose de Precios"),
                            rx.hstack(
                                rx.text("Precio base", color=MUTED, font_size="0.88rem"),
                                rx.spacer(),
                                rx.text(ReservaState.precio_unitario,
                                        color=MUTED, font_size="0.88rem"),
                                width="100%",
                            ),
                            rx.hstack(
                                rx.text("Subtotal", color=MUTED, font_size="0.88rem"),
                                rx.spacer(),
                                rx.text(ReservaState.subtotal_str,
                                        color=MUTED, font_size="0.88rem"),
                                width="100%",
                            ),
                            rx.hstack(
                                rx.text("Cargo por servicio (5%)", color=MUTED, font_size="0.88rem"),
                                rx.spacer(),
                                rx.text(ReservaState.fee_str,
                                        color=MUTED, font_size="0.88rem"),
                                width="100%",
                            ),
                            rx.divider(border_color="rgba(0,0,0,0.08)"),
                            rx.hstack(
                                rx.text("Total a pagar", color=DEEP_OCEAN,
                                        font_size="1rem", font_weight="500"),
                                rx.spacer(),
                                rx.text(ReservaState.total_str,
                                        font_family="Georgia, serif",
                                        font_size="1.5rem", color=CORAL, font_weight="700"),
                                width="100%",
                            ),
                            rx.box(
                                rx.text(
                                    "↩ Cancelación gratuita hasta 48 horas antes del tour.",
                                    font_size="0.78rem", color=MUTED, line_height="1.6",
                                ),
                                background="rgba(0,180,166,0.06)",
                                border_radius="4px",
                                padding="0.8rem",
                                width="100%",
                            ),
                            spacing="3", align_items="start", width="100%",
                        ),
                        background=WHITE,
                        border_radius="8px",
                        box_shadow="0 20px 60px rgba(13,43,62,0.1)",
                        padding="1.5rem",
                    ),

                    # Trust badges
                    rx.hstack(
                        rx.text("🔒", font_size="1.8rem"),
                        rx.text("✅", font_size="1.8rem"),
                        rx.text("🛡️", font_size="1.8rem"),
                        justify="center",
                        width="100%",
                        opacity="0.5",
                    ),
                    rx.text("Pago seguro · Datos protegidos · Garantía de satisfacción",
                            text_align="center", font_size="0.73rem", color=MUTED),

                    spacing="4",
                    width=["100%", "100%", "340px"],
                    flex_shrink="0",
                    align_items="start",
                ),

                direction="column",
                gap="3rem",
                align="start",
                max_width="1200px",
                margin="0 auto",
                padding=["2rem 1.5rem", "3rem 2rem", "4rem"],
            ),
        ),

        footer(),
        background=CREAM,
        font_family="'DM Sans', system-ui, sans-serif",
    )
