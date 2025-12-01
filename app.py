import streamlit as st
import requests
from datetime import date

# -----------------------------
# CONFIGURACIÓN BÁSICA PÁGINA
# -----------------------------
st.set_page_config(
    page_title="RentMatch - Solicitud de piso",
    page_icon="🏡",
    layout="wide",
)

WEBHOOK_SOLICITUDES = "https://gabrielisdi.app.n8n.cloud/webhook/nueva-solicitud"

# Piso simulado (vendrá de M4 en el futuro)
selected_flat = {
    "id_piso": "demo-123",
    "titulo": "Piso reformado en Salamanca",
    "barrio_ciudad": "Salamanca, Madrid",
    "precio": 1200,
    "m2": 65,
    "num_habitaciones": 2,
    "acepta_mascotas": True,
}

# -----------------------------
# ESTILOS MUY LIGEROS (SIN RECUADROS RAROS)
# -----------------------------
st.markdown(
    """
    <style>
    body {
        background-color: #f5f7fb;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* Header superior */
    .header-bar {
        background: #1d4ed8;
        background: linear-gradient(90deg, #1d4ed8, #3b82f6);
        border-radius: 12px;
        padding: 16px 22px;
        color: white;
        margin-bottom: 18px;
    }

    .header-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .header-subtitle {
        font-size: 0.95rem;
        opacity: 0.95;
    }

    /* Botón */
    .stButton > button {
        border-radius: 999px;
        padding: 0.5rem 1.8rem;
        font-weight: 600;
        border: none;
        background: linear-gradient(90deg, #1d4ed8, #3b82f6);
        color: white;
    }

    .stButton > button:hover {
        filter: brightness(1.07);
    }

    /* Inputs más suaves */
    .stTextInput > div > input,
    .stNumberInput > div > input,
    .stSelectbox > div > div,
    .stDateInput > div > input {
        border-radius: 6px;
        background-color: #f9fafb;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# HEADER SUPERIOR
# -----------------------------
st.markdown(
    """
    <div class="header-bar">
        <div class="header-title">RentMatch – Madrid</div>
        <div class="header-subtitle">
            Cuéntanos quién eres y por qué te encaja este piso.
            Usaremos tus datos para ayudar al propietario a conocerte mejor.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")  # pequeño espacio, sin recuadros

# -----------------------------
# LAYOUT: DOS COLUMNAS LIMPIAS
# -----------------------------
col_info, col_form = st.columns([0.9, 1.4])

# =========================================================
# COLUMNA IZQUIERDA – INFORMACIÓN DEL PISO
# =========================================================
with col_info:
    st.subheader("Piso seleccionado")

    st.markdown(f"**{selected_flat['titulo']}**")
    st.markdown(
        f"{selected_flat['barrio_ciudad']} · "
        f"{selected_flat.get('num_habitaciones', '?')} hab. · "
        f"{selected_flat.get('m2', '?')} m²"
    )

    precio = selected_flat.get("precio")
    acepta_mascotas = selected_flat.get("acepta_mascotas", False)

    st.markdown(
        f"<span style='font-size:1.2rem; font-weight:700; color:#16a34a;'>{precio} €/mes</span>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.caption(
        "Esta es una versión demo. Más adelante este bloque vendrá del asistente "
        "de búsqueda (M4), con fotos reales, mapa y más detalles del piso."
    )

    st.write(f"- **ID del piso:** `{selected_flat['id_piso']}`")
    st.write(f"- **Acepta mascotas:** {'✅ Sí' if acepta_mascotas else '❌ No'}")

# =========================================================
# COLUMNA DERECHA – FORMULARIO COMPLETO
# =========================================================
with col_form:
    st.subheader("Completa tu solicitud")

    with st.form("form_solicitud_completo"):

        st.markdown("**Datos personales**")
        nombre = st.text_input("Nombre y apellidos")
        email = st.text_input("Email de contacto")
        telefono = st.text_input("Teléfono de contacto")

        st.markdown("**Situación laboral y económica**")
        col_a, col_b, col_c = st.columns([1, 1, 1])
        with col_a:
            edad = st.number_input("Edad", min_value=18, max_value=100, step=1)
        with col_b:
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
        with col_c:
            ingresos_mensuales = st.number_input(
                "Ingresos netos mensuales (€)", min_value=0, step=100
            )

        tipo_contrato = st.selectbox(
            "Tipo de contrato (si aplica)",
            ["No aplica", "Indefinido", "Temporal (> 1 año)", "Temporal (≤ 1 año)"],
        )

        st.markdown("**Composición del hogar**")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            num_ocupantes = st.number_input(
                "Personas que vivirán en el piso",
                min_value=1,
                max_value=10,
                step=1,
                value=1,
            )
        with col2:
            hay_ninos = st.radio("¿Hay niños en el hogar?", ["No", "Sí"], index=0)
        with col3:
            mascotas = st.radio("¿Tienes mascotas?", ["No", "Sí"], index=0)

        tipo_mascotas = ""
        if mascotas == "Sí":
            tipo_mascotas = st.text_input("¿Qué tipo de mascotas tienes?")

        st.markdown("**Preferencias sobre el piso**")
        max_alquiler = st.number_input(
            "Alquiler máximo que estás dispuesto a pagar (€ / mes)",
            min_value=0,
            step=50,
            value=int(selected_flat.get("precio", 0))
            if selected_flat.get("precio")
            else 0,
        )

        col_p1, col_p2, col_p3 = st.columns([1, 1, 1])
        with col_p1:
            necesita_amueblado = st.selectbox(
                "¿Necesitas que esté amueblado?",
                ["Indiferente", "Sí", "No"],
            )
        with col_p2:
            necesita_ascensor = st.selectbox(
                "¿Necesitas ascensor?",
                ["Indiferente", "Sí", "No"],
            )
        with col_p3:
            admite_mascotas = st.selectbox(
                "¿Buscas piso que admita mascotas?",
                ["Indiferente", "Sí", "No"],
            )

        col_f1, col_f2 = st.columns([1, 1])
        with col_f1:
            fecha_entrada = st.date_input(
                "¿Desde qué fecha podrías entrar?",
                value=date.today(),
            )
        with col_f2:
            duracion_prevista_meses = st.number_input(
                "Duración prevista del alquiler (meses)",
                min_value=6,
                max_value=120,
                step=6,
                value=12,
            )

        st.markdown("**Preséntate al propietario**")
        texto_presentacion = st.text_area(
            "Cuéntale quién eres, qué haces y por qué este piso encaja contigo.",
            height=140,
        )

        submitted = st.form_submit_button("Enviar solicitud")

    # -----------------------------
    # LÓGICA DE ENVÍO
    # -----------------------------
    if submitted:
        if not nombre or not email:
            st.error("Por favor, rellena al menos tu nombre y email.")
        else:
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

            try:
                response = requests.post(WEBHOOK_SOLICITUDES, json=payload)
                response.raise_for_status()
                st.success("✅ Solicitud enviada correctamente. ¡Gracias!")
            except Exception as e:
                st.error(f"❌ Error enviando solicitud: {e}")

            with st.expander("Ver JSON enviado"):
                st.json(payload)
