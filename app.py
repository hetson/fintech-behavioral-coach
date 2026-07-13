import streamlit as st
from agent import procesar_mensaje_coach

# Configuración de la página
st.set_page_config(page_title="Nudge AI - Prevención de Riesgo", page_icon="🦉", layout="wide")

# --- SIMULACIÓN DE BASE DE DATOS DEL BANCO ---
datos_cliente = {
    "ingreso_mensual": 5000,
    "cuota_credito": 1200,
    "dias_para_pago": 8,
    "presupuesto_consumo": 1500,
    "gasto_actual_consumo": 1350,  # ¡Está cerca del límite!
    "meses_pago_perfecto": 3,
    "meta_recompensa": 6 # Meses necesarios para bajar la tasa
}

# --- BARRA LATERAL: DASHBOARD FINANCIERO ---
with st.sidebar:
    st.header("🏦 Perfil Crediticio")
    st.markdown("Datos monitoreados desde la Caja de Ahorro.")
    
    st.metric(label="Saldo Disponible (Estimado)", value=f"Bs. {datos_cliente['ingreso_mensual'] - datos_cliente['gasto_actual_consumo']}")
    st.metric(label="Días para el pago de cuota", value=f"{datos_cliente['dias_para_pago']} días", delta="- Próximo a vencer", delta_color="inverse")
    
    st.divider()
    
    st.subheader("📊 Control de Presupuesto")
    porcentaje_gasto = (datos_cliente['gasto_actual_consumo'] / datos_cliente['presupuesto_consumo'])
    st.progress(porcentaje_gasto, text=f"Consumo: {porcentaje_gasto*100:.0f}% del límite mensual")
    if porcentaje_gasto > 0.8:
        st.warning("⚠️ Alerta Conductual: Velocidad de gasto alta.")
        
    st.divider()
    
    # --- SISTEMA DE RECOMPENSAS (Contrato de Ulises) ---
    st.subheader("🏆 Plan de Recompensas")
    st.info("Mantén tu flujo estable para desbloquear beneficios.")
    progreso_meta = datos_cliente['meses_pago_perfecto'] / datos_cliente['meta_recompensa']
    st.progress(progreso_meta, text=f"Racha: {datos_cliente['meses_pago_perfecto']} de {datos_cliente['meta_recompensa']} meses")
    st.success("✨ Próxima recompensa: Reducción de 0.5% en Tasa de Interés.")

# Creamos un string con el contexto para enviárselo a Nudge AI
contexto_financiero_str = (
    f"El cliente tiene un gasto actual del {porcentaje_gasto*100:.0f}% de su presupuesto de consumo. "
    f"Faltan {datos_cliente['dias_para_pago']} días para que pague su cuota de Bs. {datos_cliente['cuota_credito']}. "
    f"Lleva {datos_cliente['meses_pago_perfecto']} meses de pago perfecto. Si llega a {datos_cliente['meta_recompensa']} meses, "
    f"el banco le bajará la tasa de interés en 0.5%."
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