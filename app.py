import streamlit as st
import requests
from datetime import date

st.set_page_config(layout="wide")

WEBHOOK_SOLICITUDES = "https://gabrielisdi.app.n8n.cloud/webhook/nueva-solicitud"

# ---------------------------------------------------------
# CSS
# ---------------------------------------------------------
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}

/* Banner superior */
.big-banner {
    background: linear-gradient(90deg, #2a60ff, #68a8ff);
    padding: 40px;
    border-radius: 16px;
    color: white;
    margin-bottom: 25px;
}

/* Tarjeta genérica */
.card {
    background-color: white;
    padding: 28px 30px;
    border-radius: 16px;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.08);
}

/* Títulos */
.card h2 {
    margin-top: 0;
    margin-bottom: 18px;
}

.section-subtitle {
    font-size: 18px;
    font-weight: 600;
    margin-top: 22px;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# BANNER SUPERIOR
# ---------------------------------------------------------
st.markdown("""
<div class="big-banner">
    <h1>RentMatch – Madrid</h1>
    <p>
        Cuéntanos quién eres y por qué te encaja este piso.
        Usaremos tus datos para ayudar al propietario a conocerte mejor.
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")  # pequeño espacio

# ---------------------------------------------------------
# LAYOUT PRINCIPAL: SOLO DOS TARJETAS (IZQ / DCHA)
# ---------------------------------------------------------
col_izq, col_dcha = st.columns([1, 1.3])

# =========================================================
# TARJETA IZQUIERDA: INFORMACIÓN DEL PISO
# =========================================================
with col_izq:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.markdown("## Piso seleccionado")

    st.markdown("### Piso reformado en Salamanca")
    st.write("Salamanca, Madrid · 2 hab. · 65 m²")
    st.markdown("<h3 style='color:#15803d;'>1200 €/mes</h3>", unsafe_allow_html=True)

    st.markdown("---")
    st.write("**ID del piso:** demo-123")
    st.write("**Acepta mascotas:** Sí")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TARJETA DERECHA: FORMULARIO COMPLETO
# =========================================================
with col_dcha:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.markdown("## Completa tu solicitud")

    # -------- Datos personales --------
    st.markdown("<div class='section-subtitle'>Datos personales</div>", unsafe_allow_html=True)
    nombre = st.text_input("Nombre y apellidos")
    email = st.text_input("Email de contacto")
    telefono = st.text_input("Número de contacto")

    # -------- Situación laboral y económica --------
    st.markdown("<div class='section-subtitle'>Situación laboral y económica</div>", unsafe_allow_html=True)
    edad = st.number_input("Edad", min_value=18, max_value=99, value=30)
    situacion_laboral = st.selectbox(
        "Situación laboral",
        ["Contrato indefinido", "Contrato temporal", "Autónomo", "Estudiante", "Desempleado"]
    )
    ingresos = st.number_input("Ingresos mensuales (€)", min_value=0, value=0)
    tipo_contrato = st.selectbox("Tipo de contrato (si aplica)", ["No aplica", "Indefinido", "Temporal"])

    # -------- Composición del hogar --------
    st.markdown("<div class='section-subtitle'>Composición del hogar</div>", unsafe_allow_html=True)
    num_ocupantes = st.number_input("Personas que vivirán en el piso", min_value=1, max_value=10, value=1)
    hay_ninos = st.selectbox("¿Hay niños en el hogar?", ["No", "Sí"]) == "Sí"
    mascotas = st.selectbox("¿Tienes mascotas?", ["No", "Sí"]) == "Sí"
    tipo_mascotas = st.text_input("Tipo de mascotas") if mascotas else ""

    # -------- Preferencias --------
    st.markdown("<div class='section-subtitle'>Preferencias declaradas</div>", unsafe_allow_html=True)
    max_alquiler = st.number_input("Máximo alquiler (€)", value=1200)
    amueblado = st.selectbox("¿Necesitas que esté amueblado?", ["Sí", "No", "Indiferente"])
    ascensor = st.selectbox("¿Necesitas ascensor?", ["Sí", "No", "Indiferente"])
    mascotas_ok = st.selectbox("¿Debe aceptar mascotas?", ["Sí", "No", "Indiferente"])
    fecha_entrada = st.date_input("Fecha prevista de entrada", min_value=date.today())
    duracion_meses = st.number_input("Duración del contrato (meses)", min_value=1, value=12)

    # -------- Perfil personal --------
    st.markdown("<div class='section-subtitle'>Perfil personal</div>", unsafe_allow_html=True)
    presentacion = st.text_area("Preséntate brevemente")

    # -------- Botón dentro de la MISMA tarjeta --------
    enviar = st.button("Enviar solicitud")

    # Cerramos SOLO al final de la tarjeta derecha
    st.markdown("</div>", unsafe_allow_html=True)

    # Lógica de envío
    if enviar:
        payload = {
            "id_piso": "demo-123",
            "datos_inquilino": {
                "nombre": nombre,
                "email": email,
                "telefono": telefono,
                "edad": edad,
                "situacion_laboral": situacion_laboral,
                "ingresos_mensuales": ingresos,
                "tipo_contrato": tipo_contrato,
                "num_ocupantes": num_ocupantes,
                "hay_ninos": hay_ninos,
                "mascotas": mascotas,
                "tipo_mascotas": tipo_mascotas,
            },
            "preferencias_declaradas": {
                "max_alquiler": max_alquiler,
                "necesita_amueblado": amueblado,
                "necesita_ascensor": ascensor,
                "busca_piso_que_admita_mascotas": mascotas_ok,
                "fecha_entrada": fecha_entrada.isoformat(),
                "duracion_prevista_meses": duracion_meses,
            },
            "perfil_inquilino": {
                "presentacion": presentacion,
                "tipo_hogar": "con_ninos" if hay_ninos else "sin_ninos",
                "tiene_mascotas": mascotas,
            },
        }

        try:
            requests.post(WEBHOOK_SOLICITUDES, json=payload, timeout=10)
            st.success("✅ Solicitud enviada correctamente.")
        except Exception as e:
            st.error(f"❌ Error al enviar la solicitud: {e}")
