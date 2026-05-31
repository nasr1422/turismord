"""
Página de Descripción – TurismoRD
"""
import reflex as rx
from turismord.components.shared import (
    navbar, footer, section_tag,
    GOLD, DEEP_OCEAN, TURQUOISE, CORAL, CREAM, SAND, MUTED, WHITE
)

ITINERARIO = [
    ("D1", "Salida desde Santo Domingo",
     "Partida a las 6:00 AM desde la Zona Colonial. Viaje panorámico hacia el destino (aprox. 3 horas) con paradas de descanso en ruta."),
    ("D2", "Actividad principal",
     "Llegada al punto de inicio de la actividad. El guía dará instrucciones de seguridad y comenzará la experiencia principal del tour."),
    ("D3", "Almuerzo y descanso",
     "Almuerzo típico dominicano en establecimiento local: mangú, pollo al horno, tostones y jugo de frutas naturales."),
    ("D4", "Exploración adicional",
     "Tiempo libre para explorar el área, nadar, fotografiar y disfrutar del entorno natural. Actividades opcionales disponibles."),
    ("D5", "Regreso a Santo Domingo",
     "Salida de regreso a las 5:00 PM. Llegada estimada entre 8:00 – 9:00 PM. Entrega de recuerdos y certificado de participación."),
]

OFERTAS_DETALLE = [
    {
        "id": 1, "nombre": "Cataratas del Limón & Samaná",
        "ubicacion": "Samaná, RD", "precio": 89, "duracion": "1 día",
        "dificultad": "Moderada", "idioma": "Español / Inglés",
        "incluye": "Guía bilingüe, transporte A/R, almuerzo, seguro",
        "grupo_max": "15 personas", "descuento": 15,
        "descripcion": "Un tour completo que combina la majestuosa cascada El Limón de 52 metros de altura con un paseo en yola por la bahía de Samaná. Incluye almuerzo típico dominicano y tiempo libre en la playa. El senderismo puede realizarse a caballo o a pie por la selva tropical. Una experiencia única que combina naturaleza, cultura y gastronomía dominicana.",
        "imagen": "https://images.unsplash.com/photo-1586611292717-f828b167408c?w=1200&q=80",
        "thumbs": [
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400&q=80",
            "https://images.unsplash.com/photo-1559128010-7c1ad6e1b6a5?w=400&q=80",
            "https://images.unsplash.com/photo-1518623489648-a173ef7824f3?w=400&q=80",
        ],
        "incluye_lista": ["Transporte A/R desde SD", "Guía bilingüe certificado",
                          "Almuerzo típico incluido", "Seguro de viaje",
                          "Equipo de senderismo", "Cancelación 48h"],
    },
]


class DescState(rx.State):
    oferta_id: int = 1
    gallery_img: str = "https://images.unsplash.com/photo-1586611292717-f828b167408c?w=1200&q=80"
    current_oferta: dict = OFERTAS_DETALLE[0]

    @rx.event
    def set_gallery_img(self, img: str):
        self.gallery_img = img

    @rx.event
    def ir_a_reservar(self):
        return rx.redirect(f"/reservas?id={self.oferta_id}")


def thumb_img(src: str) -> rx.Component:
    return rx.image(
        src=src,
        width="100%",
        aspect_ratio="1",
        object_fit="cover",
        border_radius="4px",
        cursor="pointer",
        transition="opacity 0.3s",
        _hover={"opacity": "0.75"},
        on_click=DescState.set_gallery_img(src),
    )


def detail_item(label: str, value: str) -> rx.Component:
    return rx.vstack(
        rx.text(label, color=TURQUOISE, font_size="0.68rem",
                letter_spacing="0.1em", text_transform="uppercase"),
        rx.text(value, color=DEEP_OCEAN, font_size="0.9rem", font_weight="500"),
        spacing="0", align_items="start",
    )


def timeline_item(day: str, title: str, desc: str) -> rx.Component:
    return rx.hstack(
        rx.box(
            rx.text(day, color=TURQUOISE, font_family="Georgia, serif",
                    font_size="0.78rem", font_weight="700"),
            width="50px", height="50px",
            border_radius="50%",
            background=DEEP_OCEAN,
            border=f"3px solid {TURQUOISE}",
            display="flex", align_items="center",
            justify_content="center",
            flex_shrink="0",
            z_index="1",
        ),
        rx.vstack(
            rx.text(title, font_family="Georgia, serif",
                    font_size="1.1rem", font_weight="700", color=DEEP_OCEAN),
            rx.text(desc, color=MUTED, font_size="0.88rem", line_height="1.7"),
            spacing="1", align_items="start",
        ),
        align="start",
        spacing="4",
        margin_bottom="2rem",
    )


def descripcion() -> rx.Component:
    o = OFERTAS_DETALLE[0]
    return rx.box(
        navbar(),

        # ── Page Hero ──
        rx.box(
            rx.box(
                position="absolute", inset="0",
                background_image=f"url('{o['imagen']}')",
                background_size="cover",
                background_position="center",
                opacity="0.22",
            ),
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.link("Inicio", href="/", color="rgba(255,255,255,0.45)",
                                text_decoration="none", font_size="0.78rem"),
                        rx.text("›", color="rgba(255,255,255,0.25)"),
                        rx.link("Ofertas", href="/#ofertas", color="rgba(255,255,255,0.45)",
                                text_decoration="none", font_size="0.78rem"),
                        rx.text("›", color="rgba(255,255,255,0.25)"),
                        rx.text(o["nombre"], color="rgba(255,255,255,0.45)", font_size="0.78rem"),
                        align="center", spacing="2",
                    ),
                    rx.heading(
                        o["nombre"],
                        font_family="Georgia, serif",
                        font_size=["2rem", "2.8rem", "3.5rem"],
                        color=WHITE, font_weight="700",
                        line_height="1.1",
                    ),
                    rx.text(o["descripcion"][:120] + "…",
                            color="rgba(255,255,255,0.65)", font_size="0.95rem",
                            line_height="1.7", max_width="600px"),
                    spacing="4", align_items="start",
                ),
                position="relative", z_index="1",
                max_width="1200px", margin="0 auto",
                padding_x=["1.5rem", "2rem", "4rem"],
            ),
            min_height="50vh",
            display="flex",
            align_items="flex-end",
            padding_bottom="3rem",
            padding_top="6rem",
            background=f"linear-gradient(165deg, {DEEP_OCEAN}, #0e3a52)",
            position="relative",
            overflow="hidden",
        ),

        # ── Main Layout ──
        rx.flex(
            # Left column
            rx.vstack(
                # Gallery
                rx.vstack(
                    rx.image(
                        src=DescState.gallery_img,
                        width="100%",
                        border_radius="6px",
                        aspect_ratio="16/9",
                        object_fit="cover",
                    ),
                    rx.grid(
                        *[thumb_img(t) for t in o["thumbs"]],
                        columns="3", gap="0.7rem", width="100%",
                    ),
                    spacing="3", width="100%",
                ),

                # Description
                rx.vstack(
                    section_tag("Descripción General"),
                    rx.heading(o["nombre"], font_family="Georgia, serif",
                               font_size="2rem", font_weight="700", color=DEEP_OCEAN),
                    rx.text(o["descripcion"], color=MUTED, line_height="1.8",
                            font_size="0.95rem"),
                    spacing="3", align_items="start", width="100%",
                    margin_top="2rem",
                ),

                # Details grid
                rx.vstack(
                    section_tag("Detalles"),
                    rx.grid(
                        detail_item("Duración", o["duracion"]),
                        detail_item("Ubicación", o["ubicacion"]),
                        detail_item("Dificultad", o["dificultad"]),
                        detail_item("Idioma", o["idioma"]),
                        detail_item("Incluye", o["incluye"]),
                        detail_item("Grupo máx.", o["grupo_max"]),
                        columns="2", gap="1rem",
                        background=SAND,
                        border_radius="8px",
                        padding="1.5rem",
                        width="100%",
                    ),
                    spacing="3", align_items="start", width="100%",
                    margin_top="2rem",
                ),

                spacing="0",
                align_items="start",
                flex="1",
                min_width="0",
            ),

            # Right sidebar
            rx.vstack(
                rx.box(
                    rx.vstack(
                        section_tag("Precio por persona"),
                        rx.hstack(
                            rx.text(f"${o['precio']}", font_family="Georgia, serif",
                                    font_size="2.5rem", font_weight="700", color=CORAL),
                            rx.text("/ persona", color=MUTED, font_size="0.85rem",
                                    align_self="flex-end", padding_bottom="0.4rem"),
                        ),
                        rx.divider(border_color="rgba(0,0,0,0.08)"),
                        rx.vstack(
                            *[rx.hstack(
                                rx.text("✓", color=TURQUOISE, font_weight="700"),
                                rx.text(item, font_size="0.85rem", color=MUTED),
                                spacing="2",
                            ) for item in o["incluye_lista"]],
                            spacing="2", align_items="start",
                        ),
                        rx.divider(border_color="rgba(0,0,0,0.08)"),
                        rx.button(
                            "🌴  Reservar este tour",
                            on_click=DescState.ir_a_reservar,
                            width="100%",
                            background=f"linear-gradient(135deg, {CORAL}, #d45038)",
                            color=WHITE,
                            padding="0.9rem",
                            border_radius="4px",
                            font_size="0.9rem",
                            cursor="pointer",
                            _hover={"filter": "brightness(1.08)"},
                        ),
                        rx.text("↩ Cancelación gratuita hasta 48h antes",
                                font_size="0.73rem", color=MUTED,
                                text_align="center"),
                        spacing="4", align_items="start", width="100%",
                    ),
                    background=WHITE,
                    border_radius="8px",
                    box_shadow="0 20px 60px rgba(13,43,62,0.12)",
                    padding="1.8rem",
                    position="sticky",
                    top="6rem",
                ),

                # Review snippet
                rx.box(
                    rx.vstack(
                        rx.text("⭐⭐⭐⭐⭐", font_size="1rem"),
                        rx.text(
                            '"Una experiencia increíble. El guía fue excelente y todo estuvo perfectamente organizado."',
                            font_size="0.85rem", color=MUTED, line_height="1.6",
                            font_style="italic",
                        ),
                        rx.text("— María G., Santo Domingo",
                                font_size="0.8rem", font_weight="600", color=DEEP_OCEAN),
                        spacing="2", align_items="start",
                    ),
                    background=SAND,
                    border_radius="8px",
                    padding="1.5rem",
                    margin_top="1rem",
                ),

                width=["100%", "100%", "360px"],
                flex_shrink="0",
                align_items="start",
            ),

            direction="column",
            gap="3rem",
            align="start",
            max_width="1200px",
            margin="0 auto",
            padding=["2rem 1.5rem", "3rem 2rem", "5rem 4rem"],
        ),

        # ── Itinerario ──
        rx.box(
            rx.vstack(
                section_tag("Día a día"),
                rx.heading(
                    "Itinerario del Tour",
                    font_family="Georgia, serif",
                    font_size="2rem", font_weight="700", color=DEEP_OCEAN,
                ),
                rx.box(
                    *[timeline_item(day, title, desc) for day, title, desc in ITINERARIO],
                    border_left=f"2px solid {TURQUOISE}",
                    padding_left="2rem",
                    margin_left="1.5rem",
                    position="relative",
                ),
                spacing="6",
                align_items="start",
                max_width="800px",
                margin="0 auto",
                width="100%",
            ),
            padding=["3rem 1.5rem", "4rem 2rem", "5rem 4rem"],
            background=SAND,
        ),

        footer(),
        background=CREAM,
        font_family="'DM Sans', system-ui, sans-serif",
    )
