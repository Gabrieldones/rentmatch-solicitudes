import streamlit as st
import requests
from datetime import date

st.set_page_config(layout="wide")

# ---------------------------------------------------------
# CSS PERSONALIZADO
# ---------------------------------------------------------
st.markdown("""
<style>

body {
    background-color: #f5f7fa;
}

.big-banner {
    background: linear-gradient(90deg, #2a60ff, #68a8ff);
    padding: 45px;
    border-radius: 12px;
    color: white;
    margin-bottom: 20px;
}

.section-title {
    font-size: 32px;
    font-weight: bold;
    margin-top: 10px;
}

.card {
    background-color: white;
    padding: 28px;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    margin-bottom: 25px;
}

/* FIX: elimina el espacio en blanco fantasma */
.form-card {
    margin-top: 0 !important;
}

.form-title {
    font-size: 26px;
    font-weight: bold;
    margin-bottom: 12px;
}

.subtitle {
    font-size: 20px;
    margin-top: 18px;
    margin-bottom: 8px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# BANNER SUPERIOR
# ---------------------------------------------------------
st.markdown("""
<div class="big-banner">
    <h1>RentMatch – Madrid</h1>
    <p>Cuéntanos quién eres y por qué te encaja este piso.  
    Usaremos tus datos para ayudar al propietario a conocerte mejor.</p>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# CONTENEDOR PRINCIPAL: DOS COLUMNAS
# ---------------------------------------------------------
col1, col2 = st.columns([1, 1.3])  # col2 ligeramente más grande


# ---------------------------------------------------------
# COLUMNA IZQUIERDA — Información del piso seleccionado
# ---------------------------------------------------------
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.markdown("<h2>Piso seleccionado</h2>", unsafe_allow_html=True)

    st.subheader("Piso reformado en Salamanca")
    st.write("Salamanca, Madrid · 2 hab. · 65 m²")
    st.markdown("<h3 style='color:#1c8c3f;'>1200 €/mes</h3>", unsafe_allow_html=True)

    st.markdown("---")

    st.write("**ID del piso:** demo-123")
    st.write("**Acepta mascotas:** Sí")

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# COLUMNA DERECHA — FORMULARIO COMPLETO
# ---------------------------------------------------------
with col2:

    # TÍTULO DEL FORMULARIO
    st.markdown("""
        <div class='card form-card'>
            <h2 class='form-title'>Completa tu solicitud</h2>
        </div>
    """, unsafe_allow_html=True)

    # TARJETA DEL FORMULARIO
    st.markdown("<div class='card form-card'>", unsafe_allow_html=True)

    # ---------------- DATOS PERSONALES ----------------
    st.markdown("<div class='subtitle'>Datos personales</div>", unsafe_allow_html=True)

    nombre = st.text_input("Nombre y apellidos")
    email = st.text_input("Email de contacto")
    telefono = st.text_input("Número de contacto")

    # ---------------- SITUACIÓN ECONÓMICA ----------------
    st.markdown("<div class='subtitle'>Situación laboral y económica</div>", unsafe_allow_html=True)

    edad = st.number_input("Edad", min_value=18, max_value=99, value=30)

    situacion_laboral = st.selectbox(
        "Situación laboral",
        ["Contrato indefinido", "Contrato temporal", "Autónomo", "Estudiante", "Desempleado"]
    )

    ingresos = st.number_input("Ingresos mensuales (€)", min_value=0, value=0)

    tipo_contrato = st.selectbox("Tipo de contrato (si aplica)", ["No aplica", "Indefinido", "Temporal"])

    # ---------------- COMPOSICIÓN DEL HOGAR ----------------
    st.markdown("<div class='subtitle'>Composición del hogar</div>", unsafe_allow_html=True)

    num_ocupantes = st.number_input("Personas que vivirán en el piso", min_value=1, max_value=10, value=1)

    hay_ninos = st.selectbox("¿Hay niños en el hogar?", ["No", "Sí"]) == "Sí"

    mascotas = st.selectbox("¿Tienes mascotas?", ["No", "Sí"]) == "Sí"

    tipo_mascotas = st.text_input("Tipo de mascotas") if mascotas else ""

    # ---------------- PREFERENCIAS ----------------
    st.markdown("<div class='subtitle'>Preferencias declaradas</div>", unsafe_allow_html=True)

    max_alquiler = st.number_input("Máximo alquiler (€)", value=1200)

    amueblado = st.selectbox("¿Necesitas que esté amueblado?", ["Sí", "No", "Indiferente"])

    ascensor = st.selectbox("¿Necesitas ascensor?", ["Sí", "No", "Indiferente"])

    mascotas_ok = st.selectbox("¿Debe aceptar mascotas?", ["Sí", "No", "Indiferente"])

    fecha_entrada = st.date_input("Fecha prevista de entrada", min_value=date.today())

    duracion_meses = st.number_input("Duración del contrato (meses)", min_value=1, value=12)

    # ---------------- PERFIL PERSONAL ----------------
    st.markdown("<div class='subtitle'>Perfil personal</div>", unsafe_allow_html=True)

    presentacion = st.text_area("Preséntate brevemente")

    # CERRAMOS TARJETA DEL FORMULARIO
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    enviar = st.button("Enviar solicitud", type="primary")

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
                "tipo_mascotas": tipo_mascotas
            },
            "preferencias_declaradas": {
                "max_alquiler": max_alquiler,
                "necesita_amueblado": amueblado,
                "necesita_ascensor": ascensor,
                "busca_piso_que_admita_mascotas": mascotas_ok,
                "fecha_entrada": fecha_entrada.isoformat(),
                "duracion_prevista_meses": duracion_meses
            },
            "perfil_inquilino": {
                "presentacion": presentacion,
                "tipo_hogar": "con_ninos" if hay_ninos else "sin_ninos",
                "tiene_mascotas": mascotas
            }
        }

        # Enviar a n8n
        try:
            requests.post("https://gabrielisdi.app.n8n.cloud/webhook/nueva-solicitud", json=payload)
            st.success("✅ Solicitud enviada correctamente.")
        except:
            st.error("❌ Error al enviar la solicitud.")
