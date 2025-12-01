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
# ESTILOS PERSONALIZADOS + HERO
# -----------------------------
st.markdown(
    """
    <style>
    /* Fondo general */
    .main {
        background: #f3f6fb;
    }

    /* Elimina márgenes */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }

    /* Tarjetas */
    .card {
        background: #ffffff;
        border-radius: 18px;
        padding: 1.6rem 1.8rem;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
    }

    /* HERO - Imagen Gran Vía */
    .hero-img-container {
        position: relative;
        height: 180px;
        border-radius: 22px;
        overflow: hidden;
        box-shadow: 0 10px 28px rgba(0,0,0,0.25);
        margin-bottom: 20px;
    }

    .hero-img {
        background-image: url('https://images.unsplash.com/photo-1508050919630-b135583b29af?q=80&w=1920&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        width: 100%;
        height: 100%;
        filter: brightness(0.60);
    }

    .hero-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(90deg, rgba(29,78,216,0.75), rgba(59,130,246,0.55));
    }

    .hero-content {
        position: absolute;
        top: 20px;
        left: 26px;
        color: white;
    }

    .hero-title {
        font-size: 1.9rem;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .hero-subtitle {
        font-size: 1rem;
        opacity: 0.95;
        margin-bottom: 10px;
    }

    /* CHIP */
    .hero-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(0,0,0,0.35);
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.78rem;
        margin-top: 8px;
    }
    .hero-dot {
        width: 10px;
        height: 10px;
        background: #22c55e;
        border-radius: 50%;
        box-shadow: 0 0 6px #22c55e;
    }

    /* Formularios */
    div[data-testid="stForm"] {
        border-radius: 18px !important;
        padding: 0 !important;
    }

    /* Botón principal */
    .stButton > button {
        border-radius: 999px;
        padding: 0.5rem 1.8rem;
        font-weight: 600;
        border: none;
        background: linear-gradient(120deg, #1d4ed8, #0ea5e9);
        color: white;
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.35);
    }
    </style>

    <div class="hero-img-container">
        <div class="hero-img"></div>
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <div class="hero-title">RentMatch – Madrid</div>
            <div class="hero-subtitle">Un asistente inmobiliario que entiende tu estilo de vida, no solo tu presupuesto.</div>

            <div class="hero-chip">
                <div class="hero-dot"></div>
                Solicitud de alquiler
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# LAYOUT DOS COLUMNAS
# -----------------------------
col_info, col_form = st.columns([0.9, 1.4])

# ------- COLUMNA IZQUIERDA (INFO PISO) -------
with col_info:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("#### Piso seleccionado")
    st.markdown(f"**{selected_flat['titulo']}**")
    st.markdown(
        f"{selected_flat['barrio_ciudad']} &nbsp; • &nbsp; "
        f"{selected_flat.get('num_habitaciones', '?')} hab. &nbsp; • &nbsp; "
        f"{selected_flat.get('m2', '?')} m²"
    )

    st.markdown(
        f"<span style='font-size:1.3rem; font-weight:700; color:#16a34a;'>{selected_flat['precio']} €/mes</span>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown(
        """
        <div style="color:#64748b; font-size:0.85rem;">
        Esta es una versión demo. Más adelante este bloque vendrá del asistente
        de búsqueda (M4), con fotos reales, mapa y más detalles del piso.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"- ID del piso: `{selected_flat['id_piso']}`\n"
        f"- Acepta mascotas: {'✅ Sí' if selected_flat['acepta_mascotas'] else '❌ No'}"
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ------- COLUMNA DERECHA (FORMULARIO) -------
with col_form:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Completa tu solicitud")

    with st.form("form_solicitud_completo"):

        st.markdown("#### Datos personales")
        nombre = st.text_input("Nombre y apellidos")
        email = st.text_input("Email de contacto")
        telefono = st.text_input("Teléfono de contacto")

        st.markdown("#### Situación laboral y económica")
        colA, colB, colC = st.columns([1, 1, 1])

        with colA:
            edad = st.number_input("Edad", min_value=18, max_value=100, step=1)
        with colB:
            situacion_laboral = st.selectbox(
                "Situación laboral",
                ["Contrato indefinido", "Contrato temporal", "Autónomo", "Estudiante", "Otro"],
            )
        with colC:
            ingresos_mensuales = st.number_input("Ingresos netos mensuales (€)", min_value=0, step=100)

        tipo_contrato = st.selectbox(
            "Tipo de contrato (si aplica)",
            ["No aplica", "Indefinido", "Temporal (> 1 año)", "Temporal (≤ 1 año)"],
        )

        st.markdown("#### Composición del hogar")
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            num_ocupantes = st.number_input("Personas que vivirán en el piso", min_value=1, max_value=10, step=1)
        with col2:
            hay_ninos = st.radio("¿Hay niños en el hogar?", ["No", "Sí"])
        with col3:
            mascotas = st.radio("¿Tienes mascotas?", ["No", "Sí"])

        tipo_mascotas = ""
        if mascotas == "Sí":
            tipo_mascotas = st.text_input("¿Qué tipo de mascotas tienes?")

        st.markdown("#### Preferencias sobre el piso")

        max_alquiler = st.number_input(
            "Alquiler máximo (€ / mes)",
            min_value=0,
            step=50,
            value=int(selected_flat["precio"]),
        )

        colP1, colP2, colP3 = st.columns(3)
        with colP1:
            necesita_amueblado = st.selectbox("¿Necesitas que esté amueblado?", ["Indiferente", "Sí", "No"])
        with colP2:
            necesita_ascensor = st.selectbox("¿Necesitas ascensor?", ["Indiferente", "Sí", "No"])
        with colP3:
            admite_mascotas = st.selectbox("¿Buscas piso que admita mascotas?", ["Indiferente", "Sí", "No"])

        colF1, colF2 = st.columns(2)
        with colF1:
            fecha_entrada = st.date_input("¿Desde cuándo podrías entrar?", value=date.today())
        with colF2:
            duracion_prevista_meses = st.number_input(
                "Duración prevista (meses)", min_value=6, max_value=120, step=6, value=12
            )

        st.markdown("#### Preséntate al propietario")
        texto_presentacion = st.text_area(
            "Cuéntale quién eres, qué haces y por qué este piso encaja contigo.",
            height=140,
        )

        submitted = st.form_submit_button("Enviar solicitud")

    # -------- ENVÍO --------
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
                "id_piso": selected_flat["id_piso"],
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

    st.markdown("</div>", unsafe_allow_html=True)
