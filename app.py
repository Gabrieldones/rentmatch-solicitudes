import streamlit as st
import requests
from datetime import date

# ============================
# CONFIGURACIÓN GENERAL
# ============================
st.set_page_config(
    page_title="RentMatch - Solicitud",
    page_icon="🏡",
    layout="wide"
)

WEBHOOK_SOLICITUDES = "https://gabrielisdi.app.n8n.cloud/webhook/nueva-solicitud"

# ============================
# ESTILOS CSS PERSONALIZADOS
# ============================
st.markdown("""
<style>

body {
    background-color: #f7f9fc;
}

/* Contenedor general del formulario con padding extra */
.form-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 40px 50px !important; /* <<< AUMENTA EL ESPACIO */
    box-shadow: 0px 3px 12px rgba(0,0,0,0.08);
}

/* Card del piso */
.flat-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 30px !important;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.07);
}

/* Cabecera bonita */
.top-banner {
    background: linear-gradient(90deg, #125ccf, #5aa9ff);
    color: white;
    padding: 38px;
    border-radius: 12px;
    margin-bottom: 25px;
}

h1, h2, h3 {
    font-weight: 600;
}

.section-title {
    margin-top: 25px;
    font-size: 22px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ============================
# PISO SIMULADO (DEMO)
# ============================
selected_flat = {
    "id_piso": "demo-123",
    "titulo": "Piso reformado en Salamanca",
    "barrio_ciudad": "Salamanca, Madrid",
    "precio": 1200,
}


# ============================
# FUNCIÓN FORMULARIO COMPLETO
# ============================
def render_solicitud_piso(selected_flat):

    st.markdown("<div class='top-banner'>", unsafe_allow_html=True)
    st.markdown("## RentMatch – Madrid")
    st.markdown("Cuéntanos quién eres y por qué te encaja este piso. Usaremos tus datos para ayudar al propietario a conocerte mejor.")
    st.markdown("</div>", unsafe_allow_html=True)

    col1, colEmpty, col2 = st.columns([1, 0.15, 1.3])  
    # colEmpty crea espacio visual extra entre columnas

    # =======================
    # COLUMNA 1 → DETALLE PISO
    # =======================
    with col1:
        st.markdown("<div class='flat-card'>", unsafe_allow_html=True)
        st.markdown("### Piso seleccionado")
        st.write(f"**{selected_flat['titulo']}**")
        st.write(f"{selected_flat['barrio_ciudad']}  ·  2 hab.  ·  65 m²")
        st.markdown(f"### <span style='color:#0a8f3c;'>{selected_flat['precio']} €/mes</span>", unsafe_allow_html=True)

        st.markdown("---")
        st.write("**ID del piso:** ", selected_flat["id_piso"])
        st.write("**Acepta mascotas:**  Sí")
        st.markdown("</div>", unsafe_allow_html=True)

    # =======================
    # COLUMNA 2 → FORMULARIO
    # =======================
    with col2:
        st.markdown("<div class='form-card'>", unsafe_allow_html=True)

        st.markdown("## Completa tu solicitud")

        with st.form("form_solicitud_completo"):

            st.markdown("### Datos personales")
            nombre = st.text_input("Nombre y apellidos")
            email = st.text_input("Email de contacto")
            telefono = st.text_input("Teléfono de contacto")

            st.markdown("### Situación laboral y económica")
            edad = st.number_input("Edad", min_value=18, max_value=100, step=1)
            situacion_laboral = st.selectbox(
                "Situación laboral",
                ["Contrato indefinido", "Contrato temporal", "Autónomo", "Estudiante", "Otro"]
            )
            ingresos_mensuales = st.number_input("Ingresos netos mensuales (€)", min_value=0, step=100)
            tipo_contrato = st.selectbox("Tipo de contrato (si aplica)", ["No aplica", "Indefinido", "Temporal (> 1 año)", "Temporal (≤ 1 año)"])

            st.markdown("### Composición del hogar")
            num_ocupantes = st.number_input("Número de personas que vivirán en el piso", min_value=1, max_value=10, step=1)
            hay_ninos = st.radio("¿Hay niños?", ["No", "Sí"])
            mascotas = st.radio("¿Tienes mascotas?", ["No", "Sí"])
            tipo_mascotas = st.text_input("¿Qué tipo de mascotas tienes?") if mascotas == "Sí" else ""

            st.markdown("### Preferencias")
            max_alquiler = st.number_input("Alquiler máximo (€ / mes)", min_value=0, step=50, value=selected_flat["precio"])
            necesita_amueblado = st.selectbox("¿Necesitas piso amueblado?", ["Indiferente", "Sí", "No"])
            necesita_ascensor = st.selectbox("¿Necesitas ascensor?", ["Indiferente", "Sí", "No"])
            admite_mascotas = st.selectbox("¿Debe admitir mascotas?", ["Indiferente", "Sí", "No"])
            fecha_entrada = st.date_input("Fecha en la que podrías entrar", value=date.today())
            duracion_prevista_meses = st.number_input("Duración prevista del alquiler (meses)", min_value=6, max_value=120, step=6, value=12)

            st.markdown("### Presentación")
            texto_presentacion = st.text_area("Cuéntale al propietario quién eres y por qué te interesa este piso", height=150)

            submitted = st.form_submit_button("Enviar solicitud")

        st.markdown("</div>", unsafe_allow_html=True)

    # ============================
    # ENVÍO A N8N
    # ============================
    if submitted:

        if not nombre or not email:
            st.error("Por favor, rellena al menos tu **nombre** y **email**.")
            return

        payload = {
            "id_piso": selected_flat["id_piso"],
            "datos_inquilino": {
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
            },
            "preferencias_declaradas": {
                "max_alquiler": max_alquiler,
                "necesita_amueblado": necesita_amueblado,
                "necesita_ascensor": necesita_ascensor,
                "busca_piso_que_admita_mascotas": admite_mascotas,
                "fecha_entrada": fecha_entrada.isoformat(),
                "duracion_prevista_meses": duracion_prevista_meses,
            },
            "perfil_inquilino": {
                "presentacion": texto_presentacion,
                "tipo_hogar": "con_ninos" if hay_ninos == "Sí" else "sin_ninos",
                "tiene_mascotas": mascotas == "Sí",
            },
        }

        try:
            response = requests.post(WEBHOOK_SOLICITUDES, json=payload)
            response.raise_for_status()
            st.success("✅ Solicitud enviada correctamente.")
        except Exception as e:
            st.error(f"❌ Error enviando solicitud: {e}")

        st.markdown("### JSON enviado")
        st.json(payload)


# Ejecutamos la interfaz
render_solicitud_piso(selected_flat)
