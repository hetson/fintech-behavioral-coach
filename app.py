import streamlit as st
from agent import procesar_mensaje_coach

# Configuración de la página
st.set_page_config(page_title="Nudge AI - Prevención de Riesgo", page_icon="🦉", layout="wide")

# --- SIMULACIÓN DE BASE DE DATOS DEL BANCO ---
# EVALUACIÓN CREDITICIA (La "Foto" al Desembolso)
evaluacion_inicial = {
    "ingreso_declarado": 5000,
    "capacidad_pago_aprobada": 1500,
    "cuota_credito": 1200
}

# MONITOREO EN TIEMPO REAL (La "Película" en Caja de Ahorro)
flujo_caja_ahorro = {
    "ingresos_reales_mes": 4800, # La realidad actual en la caja de ahorro
    "gastos_acumulados_mes": 2900,
    "saldo_actual": 1900,
    "dias_para_pago": 8,
    "meses_cumplimiento_plan": 3,
    "meta_tasa_preferencial": 6
}

# Cálculo de desviación: ¿Cómo vamos respecto a la evaluación inicial?
holgura_proyectada = evaluacion_inicial["ingreso_declarado"] - evaluacion_inicial["cuota_credito"]
holgura_real = flujo_caja_ahorro["ingresos_reales_mes"] - flujo_caja_ahorro["gastos_acumulados_mes"]

# --- BARRA LATERAL: DASHBOARD FINANCIERO EVOLUTIVO ---
with st.sidebar:
    st.header("🏦 Monitoreo Preventivo")
    st.markdown("Seguimiento de Caja de Ahorro vs Evaluación Inicial.")
    
    st.metric(label="Saldo Actual en Caja", value=f"Bs. {flujo_caja_ahorro['saldo_actual']}")
    st.metric(label="Días para cuota", value=f"{flujo_caja_ahorro['dias_para_pago']} días", delta=f"Cuota: Bs. {evaluacion_inicial['cuota_credito']}", delta_color="inverse")
    
    st.divider()
    
    st.subheader("📊 Control de Liquidez")
    # Calculamos qué porcentaje de sus ingresos reales ya se ha gastado
    porcentaje_gasto = (flujo_caja_ahorro['gastos_acumulados_mes'] / flujo_caja_ahorro['ingresos_reales_mes'])
    
    # st.progress requiere un float entre 0.0 y 1.0
    st.progress(min(porcentaje_gasto, 1.0), text=f"Consumo: {porcentaje_gasto*100:.0f}% de ingresos reales")
    if porcentaje_gasto > 0.6:
        st.warning("⚠️ Alerta Conductual: El margen de liquidez se está reduciendo.")
        
    st.divider()
    
    # --- SISTEMA DE RECOMPENSAS ---
    st.subheader("🏆 Contrato de Compromiso")
    st.info("Mantén un flujo estable en tu caja de ahorro para asegurar beneficios futuros.")
    progreso_meta = flujo_caja_ahorro['meses_cumplimiento_plan'] / flujo_caja_ahorro['meta_tasa_preferencial']
    st.progress(progreso_meta, text=f"Racha: {flujo_caja_ahorro['meses_cumplimiento_plan']} de {flujo_caja_ahorro['meta_tasa_preferencial']} meses")
    st.success("✨ Meta: Reducción de 0.5% en Tasa de Interés.")

# Creamos el string con el contexto actualizado para Nudge AI
contexto_financiero_str = (
    f"Al desembolso, el banco calculó una holgura de Bs. {holgura_proyectada}. "
    f"Hoy, su liquidez real en la caja de ahorro es de Bs. {holgura_real}. "
    f"Faltan {flujo_caja_ahorro['dias_para_pago']} días para pagar su cuota de Bs. {evaluacion_inicial['cuota_credito']}. "
    f"Está a {flujo_caja_ahorro['meta_tasa_preferencial'] - flujo_caja_ahorro['meses_cumplimiento_plan']} meses de ganar una reducción de tasa de interés."
)

# --- INTERFAZ PRINCIPAL DEL CHAT ---
st.title("🦉 Nudge AI")
st.subheader("Monitoreo Conductual y Asesoría Preventiva")
st.markdown("---")

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    st.session_state.mensajes.append({
        "rol": "assistant", 
        "contenido": "¡Hola! Veo que faltan pocos días para tu próxima cuota y estás un poco cerca del límite de tus gastos de consumo este mes. ¿Hay algo que tengas planeado comprar hoy en lo que te pueda asesorar?"
    })

for msg in st.session_state.mensajes:
    with st.chat_message(msg["rol"]):
        st.markdown(msg["contenido"])

if prompt := st.chat_input("Escribe tu mensaje (ej. 'Vi unas zapatillas en oferta y quiero comprarlas')..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.mensajes.append({"rol": "user", "contenido": prompt})
    
    with st.chat_message("assistant"):
        with st.spinner("Analizando presupuesto, riesgo y literatura conductual..."):
            # Pasamos tanto el mensaje como los datos de la barra lateral al agente
            respuesta_ia = procesar_mensaje_coach(prompt, contexto_financiero_str)
            st.markdown(respuesta_ia)
            
    st.session_state.mensajes.append({"rol": "assistant", "contenido": respuesta_ia})