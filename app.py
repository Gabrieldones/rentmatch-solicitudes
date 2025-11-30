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
    Formulario COMPLETO de solicitud de piso.
    En este paso NO se envía a n8n: solo construimos el JSON y lo mostramos.
    """

    st.markdown("### Detalle del piso seleccionado")
    st.write(
        f"**Piso:** {selected_flat.get('titulo', 'Sin título')}  \n"
        f"**ID piso:** `{selected_flat.get('id_piso')}`  \n"
        f"**Zona:** {selected_flat.get('barrio_ciudad', '–')}  \n"
        f"**Precio:** {selected_flat.get('precio', '–')} €/mes"
    )

    st.markdown("---")
    st.markdown("## Solicitud de alquiler (formulario completo)")

    with st.form("form_solicitud_completo"):
        st.markdown("### Datos personales")
        nombre = st.text_input("Nombre y apellidos", max_chars=120)
        email = st.text_input("Email de contacto")
        telefono = st.text_input("Teléfono de contacto")

        st.markdown("### Situación laboral y económica")
        edad = st.number_input("Edad", min_value=18, max_value=100, step=1)
        situacion_laboral = st.selectbox(
            "Situación laboral",
            [
                "Contrato indefinido",
                "Contrato temporal",
                "Autónomo",
                "Estudiante",
                "Otro",
            ],
        )
        ingresos_mensuales = st.number_input(
            "Ingresos netos mensuales (€)", min_value=0, step=100
        )
        tipo_contrato = st.selectbox(
            "Tipo de contrato (si aplica)",
            ["No aplica", "Indefinido", "Temporal (> 1 año)", "Temporal (≤ 1 año)"],
        )

        st.markdown("### Composición del hogar")
        num_ocupantes = st.number_input(
            "Número total de personas que vivirán en el piso",
            min_value=1,
            max_value=10,
            step=1,
            value=1,
        )
        hay_ninos = st.radio("¿Hay niños en el hogar?", ["No", "Sí"], index=0)
        mascotas = st.radio("¿Tienes mascotas?", ["No", "Sí"], index=0)
        tipo_mascotas = ""
        if mascotas == "Sí":
            tipo_mascotas = st.text_input("¿Qué tipo de mascotas tienes?")

        st.markdown("### Preferencias relacionadas con el piso")
        max_alquiler = st.number_input(
            "Alquiler máximo que estás dispuesto a pagar (€ / mes)",
            min_value=0,
            step=50,
            value=int(selected_flat.get("precio", 0)) if selected_flat.get("precio") else 0,
        )
        necesita_amueblado = st.selectbox(
            "¿Necesitas que el piso esté amueblado?",
            ["Indiferente", "Sí", "No"],
        )
        necesita_ascensor = st.selectbox(
            "¿Necesitas que el edificio tenga ascensor?",
            ["Indiferente", "Sí", "No"],
        )
        admite_mascotas = st.selectbox(
            "¿Buscas piso que admita mascotas?",
            ["Indiferente", "Sí", "No"],
        )
        fecha_entrada = st.date_input(
            "¿Desde qué fecha podrías entrar a vivir?",
            value=date.today(),
        )
        duracion_prevista_meses = st.number_input(
            "Duración prevista del alquiler (meses)",
            min_value=6,
            max_value=120,
            step=6,
            value=12,
        )

        st.markdown("### Presentación para el propietario")
        texto_presentacion = st.text_area(
            "Cuéntale brevemente quién eres, por qué te interesa este piso y "
            "qué tipo de vida harías en él.",
            height=150,
        )

        submitted = st.form_submit_button("Enviar solicitud (demo)")

    if submitted:
        if not nombre or not email:
            st.error("Por favor, rellena al menos tu nombre y email.")
            return

        # --- Construimos el JSON exactamente como lo usaremos en n8n ---

        datos_inquilino = {
            "nombre": nombre,
            "email": email,
            "telefono": telefono,
            "edad": edad,
            "situacion_laboral": situacion_laboral,
            "ingresos_mensuales": ingresos_mensuales,
            "tipo_contrato": tipo_contrato,
            "num_ocupantes": num_ocupantes,
            "hay_ninos": hay_ninos == "Sí",
            "mascotas": mascotas == "Sí",
            "tipo_mascotas": tipo_mascotas,
        }

        preferencias_declaradas = {
            "max_alquiler": max_alquiler,
            "necesita_amueblado": necesita_amueblado,
            "necesita_ascensor": necesita_ascensor,
            "busca_piso_que_admita_mascotas": admite_mascotas,
            "fecha_entrada": fecha_entrada.isoformat(),
            "duracion_prevista_meses": duracion_prevista_meses,
        }

        perfil_inquilino = {
            "presentacion": texto_presentacion,
            "tipo_hogar": "con_ninos" if hay_ninos == "Sí" else "sin_ninos",
            "tiene_mascotas": mascotas == "Sí",
        }

        payload = {
            "id_piso": selected_flat.get("id_piso"),
            "datos_inquilino": datos_inquilino,
            "preferencias_declaradas": preferencias_declaradas,
            "perfil_inquilino": perfil_inquilino,
        }

        st.success("✅ Solicitud construida correctamente (demo, sin enviar a n8n).")

        st.markdown("### JSON preparado para n8n (solo visualización)")
        st.json(payload)


# Llamamos a la función para pintar el formulario del piso simulado
render_solicitud_piso(selected_flat)
