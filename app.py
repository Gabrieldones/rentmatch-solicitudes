import streamlit as st
from datetime import date

st.title("Asistente Inmobiliario Inteligente 🏡🤖")
st.write("Módulo de solicitudes de inquilinos: 'Quiero este piso'.")

st.markdown("---")

# Simulamos un piso seleccionado (más adelante vendrá de M4)
selected_flat = {
    "id_piso": "demo-123",
    "titulo": "Piso de prueba en Barcelona",
    "barrio_ciudad": "Gràcia, Barcelona",
    "precio": 1200,
}


def render_solicitud_piso(selected_flat: dict):
    """
    Pinta un formulario básico de solicitud de piso.
    En este paso todavía NO se envía a n8n, solo mostramos un mensaje.
    """

    st.markdown("### Detalle del piso seleccionado")
    st.write(
        f"**Piso:** {selected_flat.get('titulo', 'Sin título')}  \n"
        f"**ID piso:** `{selected_flat.get('id_piso')}`  \n"
        f"**Zona:** {selected_flat.get('barrio_ciudad', '–')}  \n"
        f"**Precio:** {selected_flat.get('precio', '–')} €/mes"
    )

    st.markdown("---")
    st.markdown("## Solicitud de alquiler (versión simple)")

    with st.form("form_solicitud_simple"):
        nombre = st.text_input("Nombre y apellidos", max_chars=120)
        email = st.text_input("Email de contacto")
        fecha_entrada = st.date_input(
            "¿Desde qué fecha podrías entrar a vivir?",
            value=date.today(),
        )

        submitted = st.form_submit_button("Enviar solicitud")

    if submitted:
        if not nombre or not email:
            st.error("Por favor, rellena al menos tu nombre y email.")
        else:
            st.success(
                f"✅ Solicitud enviada (demo).\n\n"
                f"- Nombre: {nombre}\n"
                f"- Email: {email}\n"
                f"- Fecha de entrada: {fecha_entrada.isoformat()}\n"
                f"- ID piso: {selected_flat.get('id_piso')}"
            )


# Llamamos a la función para pintar el formulario del piso simulado
render_solicitud_piso(selected_flat)
