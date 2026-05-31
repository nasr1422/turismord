"""
Página de Inicio – TurismoRD
"""
import reflex as rx
from turismord.components.shared import (
    navbar, footer, section_tag, section_title,
    GOLD, DEEP_OCEAN, TURQUOISE, CORAL, CREAM, SAND, MUTED, WHITE
)

DEMO_OFFERS = [
    {"id": 1, "nombre": "Cataratas del Limón & Samaná", "ubicacion": "Samaná, RD",
     "descripcion_corta": "Descubre la impresionante cascada El Limón rodeada de naturaleza tropical.",
     "precio": 89, "duracion": "1 día", "descuento": 15,
     "imagen": "https://images.unsplash.com/photo-1586611292717-f828b167408c?w=600&q=80"},
    {"id": 2, "nombre": "Isla Saona – Paraíso Natural", "ubicacion": "La Romana, RD",
     "descripcion_corta": "Navega hacia la famosa Isla Saona con aguas turquesas y estrellas de mar.",
     "precio": 75, "duracion": "1 día", "descuento": None,
     "imagen": "https://images.unsplash.com/photo-1559128010-7c1ad6e1b6a5?w=600&q=80"},
    {"id": 3, "nombre": "Ciudad Colonial & Gastronomía", "ubicacion": "Santo Domingo, RD",
     "descripcion_corta": "Recorre el primer asentamiento europeo del Nuevo Mundo.",
     "precio": 55, "duracion": "Medio día", "descuento": None,
     "imagen": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=600&q=80"},
    {"id": 4, "nombre": "Punta Cana All-Inclusive", "ubicacion": "Punta Cana, RD",
     "descripcion_corta": "Experiencia completa en las mejores playas del Caribe.",
     "precio": 149, "duracion": "3 días", "descuento": 20,
     "imagen": "https://images.unsplash.com/photo-1530789253388-582c481c54b0?w=600&q=80"},
    {"id": 5, "nombre": "Jarabacoa Adventure – Rafting", "ubicacion": "Jarabacoa, RD",
     "descripcion_corta": "Adrenalina pura en el río Yaque del Norte con rafting y canopy.",
     "precio": 95, "duracion": "1 día", "descuento": None,
     "imagen": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&q=80"},
    {"id": 6, "nombre": "Los Haitises & Manglares", "ubicacion": "Samaná, RD",
     "descripcion_corta": "Navega por el parque nacional Los Haitises y sus cuevas taínas.",
     "precio": 85, "duracion": "1 día", "descuento": 10,
     "imagen": "https://images.unsplash.com/photo-1518623489648-a173ef7824f3?w=600&q=80"},
]


class HomeState(rx.State):
    busqueda_destino: str = ""
    busqueda_fecha: str = ""
    busqueda_personas: str = "2"
    contacto_nombre: str = ""
    contacto_email: str = ""
    contacto_asunto: str = ""
    contacto_mensaje: str = ""
    contacto_enviado: bool = False

    @rx.event
    def set_busqueda_destino(self, val: str):
        self.busqueda_destino = val

    @rx.event
    def set_busqueda_fecha(self, val: str):
        self.busqueda_fecha = val

    @rx.event
    def set_busqueda_personas(self, val: str):
        self.busqueda_personas = val

    @rx.event
    def buscar(self):
        return rx.redirect(f"/descripcion?busqueda={self.busqueda_destino}")

    @rx.event
    def set_contacto_nombre(self, v: str): self.contacto_nombre = v
    @rx.event
    def set_contacto_email(self, v: str): self.contacto_email = v
    @rx.event
    def set_contacto_asunto(self, v: str): self.contacto_asunto = v
    @rx.event
    def set_contacto_mensaje(self, v: str): self.contacto_mensaje = v

    @rx.event
    def reset_contacto(self):
        self.contacto_enviado = False

    @rx.event
    def enviar_contacto(self):
        self.contacto_enviado = True
        self.contacto_nombre = ""
        self.contacto_email = ""
        self.contacto_asunto = ""
        self.contacto_mensaje = ""


def stat_box(number: str, label: str) -> rx.Component:
    return rx.vstack(
        rx.text(number, color=GOLD, font_family="Georgia, serif",
                font_size="2rem", font_weight="700"),
        rx.text(label, color="rgba(255,255,255,0.45)", font_size="0.72rem",
                letter_spacing="0.1em", text_transform="uppercase"),
        align_items="center", spacing="1",
    )


def offer_card(o: dict) -> rx.Component:
    has_discount = o["descuento"] is not None
    return rx.link(
        rx.box(
            # Image
            rx.box(
                rx.image(
                    src=o["imagen"],
                    width="100%", height="100%",
                    object_fit="cover",
                    transition="transform 0.5s",
                    _hover={"transform": "scale(1.06)"},
                ),
                rx.cond(
                    has_discount,
                    rx.box(
                        rx.text(f"{o['descuento']}% OFF", color=WHITE,
                                font_size="0.68rem", font_weight="600",
                                letter_spacing="0.08em"),
                        position="absolute", top="0.8rem", left="0.8rem",
                        background=CORAL, padding="0.25rem 0.7rem",
                        border_radius="100px",
                    ),
                    rx.box(),
                ),
                height="200px", overflow="hidden",
                position="relative",
            ),
            # Body
            rx.vstack(
                rx.hstack(
                    rx.text("📍", font_size="0.8rem"),
                    rx.text(o["ubicacion"], color=TURQUOISE, font_size="0.72rem",
                            letter_spacing="0.1em", text_transform="uppercase"),
                    spacing="1", align="center",
                ),
                rx.text(o["nombre"], font_family="Georgia, serif",
                        font_size="1.15rem", font_weight="700", color=DEEP_OCEAN,
                        line_height="1.3"),
                rx.text(o["descripcion_corta"], color=MUTED, font_size="0.85rem",
                        line_height="1.6", no_of_lines=2),
                rx.divider(border_color="rgba(0,0,0,0.07)", margin_y="0.3rem"),
                rx.hstack(
                    rx.text(f"${o['precio']}", font_family="Georgia, serif",
                            font_size="1.4rem", font_weight="700", color=DEEP_OCEAN),
                    rx.text("/ persona", color=MUTED, font_size="0.75rem"),
                    rx.spacer(),
                    rx.text(f"🕐 {o['duracion']}", color=MUTED, font_size="0.8rem"),
                    align="center", width="100%",
                ),
                padding="1.2rem",
                spacing="2",
                align_items="start",
            ),
            background=WHITE,
            border_radius="8px",
            overflow="hidden",
            box_shadow="0 20px 60px rgba(13,43,62,0.1)",
            transition="transform 0.3s, box-shadow 0.3s",
            _hover={
                "transform": "translateY(-6px)",
                "box_shadow": "0 30px 80px rgba(13,43,62,0.18)",
            },
            cursor="pointer",
        ),
        href=f"/descripcion?id={o['id']}",
        text_decoration="none",
    )


def search_form() -> rx.Component:
    input_style = {
        "width": "100%",
        "padding": "0.7rem 0.9rem",
        "background": "rgba(255,255,255,0.08)",
        "border": "1px solid rgba(255,255,255,0.15)",
        "border_radius": "4px",
        "color": WHITE,
        "font_size": "0.88rem",
    }
    label_style = {
        "font_size": "0.7rem",
        "letter_spacing": "0.1em",
        "text_transform": "uppercase",
        "color": "rgba(255,255,255,0.5)",
        "margin_bottom": "0.3rem",
    }

    return rx.box(
        rx.vstack(
            rx.heading("Busca tu próxima aventura",
                       font_family="Georgia, serif", color=WHITE,
                       font_size="1.25rem", font_weight="700"),
            rx.vstack(
                rx.text("Destino", **label_style),
                rx.input(
                    placeholder="Samaná, Punta Cana, Jarabacoa…",
                    value=HomeState.busqueda_destino,
                    on_change=HomeState.set_busqueda_destino,
                    **input_style,
                ),
                spacing="1", width="100%",
            ),
            rx.vstack(
                rx.text("Fecha de viaje", **label_style),
                rx.input(
                    type="date",
                    value=HomeState.busqueda_fecha,
                    on_change=HomeState.set_busqueda_fecha,
                    **input_style,
                ),
                spacing="1", width="100%",
            ),
            rx.vstack(
                rx.text("Número de personas", **label_style),
                rx.select(
                    ["1 persona", "2 personas", "3 personas", "4 personas", "5+ personas"],
                    value=HomeState.busqueda_personas,
                    on_change=HomeState.set_busqueda_personas,
                    **input_style,
                ),
                spacing="1", width="100%",
            ),
            rx.button(
                "🔍  Buscar Tours",
                on_click=HomeState.buscar,
                width="100%",
                background=f"linear-gradient(135deg, {TURQUOISE}, #009e92)",
                color=WHITE,
                padding="0.85rem",
                border_radius="4px",
                font_size="0.9rem",
                font_weight="500",
                cursor="pointer",
                _hover={"filter": "brightness(1.1)"},
                margin_top="0.5rem",
            ),
            spacing="4",
            width="100%",
        ),
        background="rgba(255,255,255,0.07)",
        border="1px solid rgba(255,255,255,0.12)",
        backdrop_filter="blur(20px)",
        border_radius="8px",
        padding="1.8rem",
        width=["100%", "100%", "420px"],
    )


def hero_section() -> rx.Component:
    return rx.box(
        # Background
        rx.box(
            position="absolute", inset="0",
            background_image="url('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1800&q=80')",
            background_size="cover",
            background_position="center",
            opacity="0.18",
        ),
        # Content
        rx.box(
            rx.flex(
                # Left text
                rx.vstack(
                    rx.box(
                        rx.text("◆  República Dominicana",
                                color=GOLD, font_size="0.7rem",
                                letter_spacing="0.15em", text_transform="uppercase"),
                        background="rgba(201,168,76,0.12)",
                        border="1px solid rgba(201,168,76,0.35)",
                        padding="0.4rem 1rem",
                        border_radius="100px",
                        display="inline-block",
                    ),
                    rx.heading(
                        "Explora el ",
                        rx.text.span("Paraíso Caribeño",
                                     color=TURQUOISE, font_style="italic",
                                     display="block"),
                        font_family="Georgia, 'Times New Roman', serif",
                        font_size=["2.8rem", "3.5rem", "5rem"],
                        font_weight="900",
                        color=WHITE,
                        line_height="1.0",
                    ),
                    rx.text(
                        "Tours exclusivos, experiencias auténticas y reservas seguras en los destinos más espectaculares de la isla.",
                        color="rgba(255,255,255,0.65)",
                        font_size="1rem",
                        line_height="1.75",
                        max_width="480px",
                    ),
                    rx.hstack(
                        rx.link(
                            rx.button(
                                "Ver Ofertas",
                                background=CORAL, color=WHITE,
                                padding="0.85rem 1.8rem",
                                border_radius="2px",
                                font_size="0.9rem",
                                cursor="pointer",
                                _hover={"background": "#d45038"},
                            ),
                            href="#ofertas",
                        ),
                        rx.link(
                            rx.button(
                                "Conocer más",
                                background="transparent",
                                color=WHITE,
                                border=f"1px solid rgba(255,255,255,0.3)",
                                padding="0.85rem 1.8rem",
                                border_radius="2px",
                                font_size="0.9rem",
                                cursor="pointer",
                                _hover={"border_color": GOLD, "color": GOLD},
                            ),
                            href="/descripcion",
                        ),
                        spacing="4",
                        flex_wrap="wrap",
                    ),
                    spacing="5",
                    align_items="start",
                    max_width="550px",
                ),
                # Right: search card
                search_form(),
                direction="column",
                gap="3rem",
                align="center",
                justify="between",
                width="100%",
                max_width="1300px",
                margin="0 auto",
                padding_x=["1.5rem", "2rem", "4rem"],
            ),
            position="relative",
            z_index="1",
            width="100%",
        ),
        min_height="100vh",
        display="flex",
        align_items="center",
        background=f"linear-gradient(165deg, {DEEP_OCEAN} 0%, #0e3a52 50%, #144a5e 100%)",
        position="relative",
        overflow="hidden",
        padding_top="5rem",
    )


def stats_bar() -> rx.Component:
    return rx.flex(
        stat_box("500+", "Tours disponibles"),
        stat_box("12K+", "Viajeros felices"),
        stat_box("25+", "Destinos"),
        stat_box("4.9 ★", "Calificación promedio"),
        background=DEEP_OCEAN,
        padding=["1.5rem 1rem", "1.5rem 2rem", "1.5rem 4rem"],
        justify="center",
        gap=["1.5rem", "2rem", "4rem"],
        flex_wrap="wrap",
    )


def ofertas_section() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.vstack(
                section_tag("Nuestras Ofertas"),
                section_title("Tours & Excursiones Destacadas"),
                rx.text(
                    "Experiencias cuidadosamente seleccionadas para que vivas la República Dominicana como nunca antes.",
                    color=MUTED, font_size="0.95rem", max_width="500px",
                    text_align="center", line_height="1.7",
                ),
                align_items="center", spacing="2",
            ),
            rx.grid(
                *[offer_card(o) for o in DEMO_OFFERS],
                columns="3",
                gap="1.8rem",
                width="100%",
                max_width="1300px",
            ),
            spacing="8",
            width="100%",
            max_width="1300px",
            margin="0 auto",
        ),
        id="ofertas",
        padding=["4rem 1.5rem", "5rem 2rem", "6rem 4rem"],
        background=CREAM,
    )


def why_us_section() -> rx.Component:
    items = [
        ("🛡️", "Reservas Seguras", "Pagos encriptados y protección total de tus datos en cada transacción."),
        ("🌟", "Guías Certificados", "Todos nuestros guías son certificados, bilingües y con años de experiencia."),
        ("↩️", "Cancelación Flexible", "Cancela hasta 48 horas antes sin penalización. Tu tranquilidad es nuestra prioridad."),
        ("🤝", "Soporte 24/7", "Nuestro equipo está disponible en todo momento para asistirte durante tu viaje."),
    ]
    return rx.box(
        rx.vstack(
            rx.vstack(
                section_tag("¿Por qué elegirnos?"),
                section_title("La experiencia que mereces"),
                align_items="center", spacing="2",
            ),
            rx.grid(
                *[rx.vstack(
                    rx.text(icon, font_size="2.5rem"),
                    rx.text(title, font_family="Georgia, serif", font_size="1.1rem",
                            font_weight="700", color=DEEP_OCEAN),
                    rx.text(desc, color=MUTED, font_size="0.88rem", line_height="1.7",
                            text_align="center"),
                    align_items="center", spacing="2",
                    padding="1.5rem",
                ) for icon, title, desc in items],
                columns="4",
                gap="1.5rem",
                width="100%",
                max_width="1100px",
            ),
            spacing="8",
            width="100%",
            max_width="1100px",
            margin="0 auto",
        ),
        padding=["4rem 1.5rem", "5rem 2rem", "6rem 4rem"],
        background="#F0EADB",
    )


def contact_section() -> rx.Component:
    input_style = {
        "width": "100%",
        "padding": "0.75rem 1rem",
        "background": "rgba(255,255,255,0.07)",
        "border": "1px solid rgba(255,255,255,0.12)",
        "border_radius": "4px",
        "color": WHITE,
        "font_size": "0.88rem",
    }
    contact_items = [
        ("📍", "Dirección", "Av. Abraham Lincoln 456, Santo Domingo, RD"),
        ("📞", "Teléfono", "+1 (809) 555-0123"),
        ("✉️", "Email", "hola@turismord.com"),
        ("🕐", "Horario", "Lun–Vie 8:00 AM – 6:00 PM · Sáb 9:00 AM – 2:00 PM"),
    ]
    return rx.box(
        rx.flex(
            # Left info
            rx.vstack(
                section_tag("Contáctanos"),
                section_title("Planifica tu aventura con nosotros", color=WHITE),
                rx.text(
                    "¿Tienes preguntas sobre algún tour o quieres un paquete personalizado? Nuestro equipo está listo para ayudarte.",
                    color="rgba(255,255,255,0.6)", line_height="1.75", font_size="0.95rem",
                ),
                *[rx.hstack(
                    rx.box(
                        rx.text(icon, font_size="1.1rem"),
                        width="44px", height="44px",
                        border_radius="50%",
                        background="rgba(201,168,76,0.12)",
                        border=f"1px solid rgba(201,168,76,0.3)",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        flex_shrink="0",
                    ),
                    rx.vstack(
                        rx.text(lbl, color=GOLD, font_size="0.68rem",
                                letter_spacing="0.1em", text_transform="uppercase"),
                        rx.text(val, color=WHITE, font_size="0.88rem"),
                        spacing="0", align_items="start",
                    ),
                    align="center", spacing="3",
                ) for icon, lbl, val in contact_items],
                spacing="4", align_items="start", max_width="460px",
            ),
            # Right form
            rx.cond(
                HomeState.contacto_enviado,
                rx.vstack(
                    rx.text("✅", font_size="3rem"),
                    rx.heading("¡Mensaje enviado!", color=WHITE,
                               font_family="Georgia, serif"),
                    rx.text("Nos pondremos en contacto contigo pronto.",
                            color="rgba(255,255,255,0.6)"),
                    rx.button(
                        "Enviar otro mensaje",
                        on_click=HomeState.reset_contacto,
                        background=TURQUOISE, color=WHITE,
                        padding="0.7rem 1.5rem", border_radius="4px", cursor="pointer",
                    ),
                    align_items="center", spacing="3", padding="2rem",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.input(placeholder="Tu nombre", value=HomeState.contacto_nombre,
                                 on_change=HomeState.set_contacto_nombre, **input_style),
                        rx.input(placeholder="Tu email", value=HomeState.contacto_email,
                                 on_change=HomeState.set_contacto_email, **input_style),
                        spacing="3", width="100%",
                    ),
                    rx.input(placeholder="Asunto", value=HomeState.contacto_asunto,
                             on_change=HomeState.set_contacto_asunto, **input_style),
                    rx.text_area(placeholder="¿En qué podemos ayudarte?",
                                 value=HomeState.contacto_mensaje,
                                 on_change=HomeState.set_contacto_mensaje,
                                 **{**input_style, "height": "120px"}),
                    rx.button(
                        "Enviar Mensaje",
                        on_click=HomeState.enviar_contacto,
                        width="100%",
                        background=CORAL, color=WHITE,
                        padding="0.9rem",
                        border_radius="2px",
                        font_size="0.9rem",
                        cursor="pointer",
                        _hover={"background": "#d45038"},
                    ),
                    spacing="3", width="100%",
                    background="rgba(255,255,255,0.06)",
                    border="1px solid rgba(255,255,255,0.1)",
                    border_radius="8px",
                    padding="1.8rem",
                ),
            ),
            direction="column",
            gap="4rem",
            align="start",
            width="100%",
            max_width="1100px",
            margin="0 auto",
        ),
        id="contacto",
        padding=["4rem 1.5rem", "5rem 2rem", "6rem 4rem"],
        background=DEEP_OCEAN,
    )


def index() -> rx.Component:
    return rx.box(
        navbar(),
        hero_section(),
        stats_bar(),
        ofertas_section(),
        why_us_section(),
        contact_section(),
        footer(),
        background=CREAM,
        font_family="'DM Sans', system-ui, sans-serif",
    )
