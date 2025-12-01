import streamlit as st
import requests
import json
from datetime import date

st.set_page_config(page_title="Solicitud de Alquiler – RentMatch", layout="wide")

# ============================
# CSS ESTILIZADO – Banner, Layout y Formularios
# ============================
st.markdown("""
<style>
/* -------- Banner superior -------- */
.top-banner {
    background: linear-gradient(90deg, #125ccf, #5aa9ff);
    color: white;
    padding: 40px 55px;
    border-radius: 14px;
    margin-bottom: 35px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.12);
}

/* -------- Tarjetas blancas -------- */
.card {
    padding: 25px;
    background: white;
    border-radius: 12px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.06);
    margin-bottom: 25px;
}

/* -------- Títulos -------- */
.section-title {
    font-size: 26px;
    font-weight: 700;
    margin-bottom: 12px;
}

/* -------- Inputs más elegantes -------- */
.stTextInput > div > input,
.stNumberInput > div > input,
.stSelectbox > div > div {
    border-radius: 8px;
    background-color: #f4f6f9;
}

</style>
""", unsafe_allow_html=True)

# ============================
# BANNER SUPERIOR (ARREGLADO)
# ============================
st.markdown("""
<div class="top-banner">
    <h1>RentMatch – Madrid</h1>
    <p style="font-size:18px; margin-top:8px;">
        Cuéntanos quién eres y por qué te encaja este piso. 
        Usaremos tus datos para ayudar al propietario a conocerte mejor.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

# ============================
# CARGA DE DATOS DEL PISO (DEMO)
# ============================
piso_demo = {
    "id_piso": "demo-123",
    "titulo": "Piso reformado en Salamanca",
    "zona": "Salamanca, Madrid",
    "habitaciones": 2,
    "metros": 65,
    "precio": 1200,
    "acepta_mascotas": True
}

# ============================
# LAYOUT PRINCIPAL: dos columnas
# ============================
col1, col2 = st.columns([1.1, 1.4])

# -------- COLUMNA IZQUIERDA: Información del piso --------
with col1:

    st.markdown("### Piso seleccionado")

    st.markdown(f"""
    <div class="card">
        <h3>{piso_demo['titulo']}</h3>
        <p>{piso_demo['zona']} · {piso_demo['habitaciones']} hab. · {piso_demo['metros']} m²</p>
        <h3 style="color:#1a8f2d;">{piso_demo['precio']} €/mes</h3>
        <hr>
        <p><b>ID del piso:</b> {piso_demo['id_piso']}</p>
        <p><b>Acepta mascotas:</b> {"Sí" if piso_demo['acepta_mascotas'] else "No"}</p>
    </div>
    """, unsafe_allow_html=True)

# -------- COLUMNA DERECHA: FORMULARIO COMPLETO --------
with col2:

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Completa tu solicitud</div>', unsafe_allow_html=True)

    # ---------------- DATOS PERSONALES ----------------
    st.subheader("Datos personales")

    nombre = st.text_input("Nombre y apellidos")
    email = st.text_input("Email de contacto")
    telefono = st.text_input("Número de contacto")

    # ---------------- DATOS ECONÓMICOS ----------------
    st.subheader("Situación laboral y económica")

    edad = st.number_input("Edad", min_value=18, max_value=99, value=30)
    situacion_laboral = st.selectbox(
        "Situación laboral",
        ["Contrato indefinido", "Contrato temporal", "Autónomo", "Estudiante", "Desempleado"]
    )
    ingresos = st.number_input("Ingresos mensuales (€)", min_value=0, value=0)
    tipo_contrato = st.selectbox("Tipo de contrato (si aplica)", ["No aplica", "Indefinido", "Temporal"])

    # ---------------- COMPOSICIÓN DEL HOGAR ----------------
    st.subheader("Composición del hogar")

    num_ocupantes = st.number_input("Personas que vivirán en el piso", min_value=1, max_value=10, value=1)
    hay_ninos = st.selectbox("¿Hay niños en el hogar?", ["No", "Sí"]) == "Sí"
    mascotas = st.selectbox("¿Tienes mascotas?", ["No", "Sí"]) == "Sí"
    tipo_mascotas = ""
    if mascotas:
        tipo_mascotas = st.text_input("Tipo de mascotas")

    # ---------------- PREFERENCIAS ----------------
    st.subheader("Preferencias declaradas")

    max_alquiler = st.number_input("Máximo alquiler que estás dispuesto a pagar (€)", value=1200)
    amueblado = st.selectbox("¿Necesitas que esté amueblado?", ["Sí", "No", "Indiferente"])
    ascensor = st.selectbox("¿Necesitas ascensor?", ["Sí", "No", "Indiferente"])
    mascotas_ok = st.selectbox("¿Debe aceptar mascotas?", ["Sí", "No", "Indiferente"])
    fecha_entrada = st.date_input("Fecha prevista de entrada", min_value=date.today())
    duracion_meses = st.number_input("Duración prevista de alquiler (meses)", min_value=1, value=12)

    # ---------------- PERFIL PERSONAL ----------------
    st.subheader("Perfil personal")

    presentacion = st.text_area("Preséntate brevemente")

    st.markdown("</div>", unsafe_allow_html=True)  # cierre del card

    st.markdown("<br>", unsafe_allow_html=True)

    # BOTÓN DE ENVÍO
    enviar = st.button("Enviar solicitud", type="primary")

    if enviar:
        payload = {
            "id_piso": piso_demo["id_piso"],
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
                "fecha_entrada": str(fecha_entrada),
                "duracion_prevista_meses": duracion_meses,
            },
            "perfil_inquilino": {
                "presentacion": presentacion,
            }
        }

        try:
            response = requests.post(
                "https://gabrielisdi.app.n8n.cloud/webhook/nueva-solicitud",
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                st.success("✅ Solicitud enviada correctamente.")
            else:
                st.error(f"❌ Error al enviar solicitud: {response.status_code}")

        except Exception as e:
            st.error(f"⚠ Error de conexión: {e}")
