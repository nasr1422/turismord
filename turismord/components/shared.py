"""
Shared UI components: Navbar and Footer
"""
import reflex as rx

GOLD = "#C9A84C"
DEEP_OCEAN = "#0D2B3E"
TURQUOISE = "#00B4A6"
CORAL = "#E8624A"
CREAM = "#FBF7EE"
SAND = "#F5EED8"
MUTED = "#7A8E97"
WHITE = "#FFFFFF"


def nav_link(label: str, href: str) -> rx.Component:
    return rx.link(
        label,
        href=href,
        color="rgba(255,255,255,0.75)",
        font_size="0.8rem",
        font_weight="500",
        letter_spacing="0.1em",
        text_transform="uppercase",
        text_decoration="none",
        _hover={"color": GOLD},
    )


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            # Logo
            rx.link(
                rx.hstack(
                    rx.text("Turismo", color=GOLD, font_family="Georgia, serif",
                            font_size="1.5rem", font_weight="700"),
                    rx.text("RD", color=TURQUOISE, font_family="Georgia, serif",
                            font_size="1.5rem", font_weight="700", font_style="italic"),
                    spacing="0",
                ),
                href="/",
                text_decoration="none",
            ),
            # Links
            rx.hstack(
                nav_link("Inicio", "/"),
                nav_link("Destinos", "/descripcion"),
                nav_link("Reservas", "/reservas"),
                spacing="8",
                display="flex",
            ),
            # CTA
            rx.link(
                rx.button(
                    "Reservar ahora",
                    background=CORAL,
                    color=WHITE,
                    border_radius="2px",
                    padding="0.55rem 1.3rem",
                    font_size="0.8rem",
                    font_weight="500",
                    letter_spacing="0.08em",
                    cursor="pointer",
                    _hover={"background": "#d45038"},
                ),
                href="/reservas",
                text_decoration="none",
            ),
            justify="between",
            align="center",
            width="100%",
            max_width="1300px",
            margin="0 auto",
            padding_x="2rem",
        ),
        position="fixed",
        top="0",
        left="0",
        right="0",
        z_index="100",
        background="rgba(10,31,46,0.95)",
        backdrop_filter="blur(12px)",
        border_bottom=f"1px solid rgba(201,168,76,0.2)",
        padding_y="1.1rem",
    )


def footer() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                # Brand
                rx.vstack(
                    rx.hstack(
                        rx.text("Turismo", color=GOLD, font_family="Georgia, serif",
                                font_size="1.3rem", font_weight="700"),
                        rx.text("RD", color=TURQUOISE, font_family="Georgia, serif",
                                font_size="1.3rem", font_style="italic"),
                        spacing="0",
                    ),
                    rx.text(
                        "La plataforma líder de turismo en la República Dominicana.",
                        color="rgba(255,255,255,0.4)", font_size="0.85rem",
                        max_width="240px", line_height="1.6",
                    ),
                    align_items="start",
                    spacing="3",
                ),
                rx.vstack(
                    rx.text("Destinos", color=GOLD, font_size="0.7rem",
                            letter_spacing="0.15em", text_transform="uppercase"),
                    rx.link("Samaná", href="#", color="rgba(255,255,255,0.4)", font_size="0.85rem", text_decoration="none"),
                    rx.link("Punta Cana", href="#", color="rgba(255,255,255,0.4)", font_size="0.85rem", text_decoration="none"),
                    rx.link("Jarabacoa", href="#", color="rgba(255,255,255,0.4)", font_size="0.85rem", text_decoration="none"),
                    rx.link("La Romana", href="#", color="rgba(255,255,255,0.4)", font_size="0.85rem", text_decoration="none"),
                    align_items="start", spacing="2",
                ),
                rx.vstack(
                    rx.text("Empresa", color=GOLD, font_size="0.7rem",
                            letter_spacing="0.15em", text_transform="uppercase"),
                    rx.link("Sobre nosotros", href="#", color="rgba(255,255,255,0.4)", font_size="0.85rem", text_decoration="none"),
                    rx.link("Blog de viajes", href="#", color="rgba(255,255,255,0.4)", font_size="0.85rem", text_decoration="none"),
                    rx.link("Trabaja con nosotros", href="#", color="rgba(255,255,255,0.4)", font_size="0.85rem", text_decoration="none"),
                    align_items="start", spacing="2",
                ),
                rx.vstack(
                    rx.text("Soporte", color=GOLD, font_size="0.7rem",
                            letter_spacing="0.15em", text_transform="uppercase"),
                    rx.link("Centro de ayuda", href="#", color="rgba(255,255,255,0.4)", font_size="0.85rem", text_decoration="none"),
                    rx.link("Términos", href="#", color="rgba(255,255,255,0.4)", font_size="0.85rem", text_decoration="none"),
                    rx.link("Cancelaciones", href="#", color="rgba(255,255,255,0.4)", font_size="0.85rem", text_decoration="none"),
                    align_items="start", spacing="2",
                ),
                justify="between",
                width="100%",
                align_items="start",
                flex_wrap="wrap",
                spacing="8",
            ),
            rx.divider(border_color="rgba(255,255,255,0.08)"),
            rx.hstack(
                rx.text("© 2025 TurismoRD. Todos los derechos reservados.",
                        color="rgba(255,255,255,0.3)", font_size="0.78rem"),
                rx.text("Hecho con ❤️ en República Dominicana",
                        color="rgba(255,255,255,0.3)", font_size="0.78rem"),
                justify="between",
                width="100%",
            ),
            spacing="6",
            width="100%",
            max_width="1200px",
            margin="0 auto",
        ),
        background=DEEP_OCEAN,
        padding="3rem 2rem 1.5rem",
        border_top=f"1px solid rgba(201,168,76,0.15)",
        margin_top="4rem",
    )


def section_tag(text: str) -> rx.Component:
    return rx.text(
        text,
        color=CORAL,
        font_size="0.72rem",
        letter_spacing="0.18em",
        text_transform="uppercase",
        font_weight="600",
        margin_bottom="0.5rem",
    )


def section_title(text: str, color: str = DEEP_OCEAN) -> rx.Component:
    return rx.heading(
        text,
        font_family="Georgia, 'Times New Roman', serif",
        font_size=["1.8rem", "2rem", "2.5rem"],
        font_weight="700",
        color=color,
        line_height="1.2",
    )
