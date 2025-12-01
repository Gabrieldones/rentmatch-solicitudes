# -----------------------------
# NUEVO HEADER ESTILO RENTMATCH
# -----------------------------
st.markdown(
    """
    <style>
    .hero-img-container {
        position: relative;
        height: 170px;
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.25);
        margin-bottom: 20px;
    }

    /* Imagen de fondo (Madrid – libre de derechos) */
    .hero-img {
        background-image: url('https://images.unsplash.com/photo-1552832230-c0197dd311b5?q=80&w=1920&auto=format&fit=crop'); 
        background-size: cover;
        background-position: center;
        width: 100%;
        height: 100%;
        filter: brightness(0.75);
    }

    /* Capa de gradiente azul */
    .hero-overlay {
        position: absolute;
        inset: 0;
        background: linear-gradient(90deg, rgba(29,78,216,0.85), rgba(59,130,246,0.75));
        backdrop-filter: blur(1px);
    }

    /* Contenido dentro de la cabecera */
    .hero-content {
        position: absolute;
        top: 18px;
        left: 22px;
        color: white;
    }

    .hero-title {
        font-size: 1.7rem;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .hero-subtitle {
        font-size: 0.90rem;
        opacity: 0.95;
        margin-bottom: 8px;
    }

    /* Chip */
    .hero-chip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(0,0,0,0.35);
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 0.75rem;
        margin-top: 6px;
    }
    .hero-dot {
        width: 10px;
        height: 10px;
        background: #22c55e;
        border-radius: 50%;
        box-shadow: 0 0 6px #22c55e;
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
                Buscando el piso ideal en Madrid
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
