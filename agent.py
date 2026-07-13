import os
from dotenv import load_dotenv
from typing import Literal, List
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from memoria_rag import buscar_contexto

load_dotenv()

class TriajeFinanciero(BaseModel):
    decision: Literal["NUDGE_REFLEXIVO", "EXPLORAR_CONTEXTO", "ESCALAR_ASESOR"] = Field(
        description="La acción que debe tomar el sistema basándose en la intención del usuario."
    )
    urgencia: Literal["BAJA", "MEDIANA", "ALTA"] = Field(
        description="Nivel de urgencia financiera o emocional."
    )
    campos_faltantes: List[str] = Field(
        default_factory=list,
        description="Si la decisión es EXPLORAR_CONTEXTO, lista qué información falta."
    )

def inicializar_motor_ia(temperatura=0.0):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("¡Error! No se encontró la variable GEMINI_API_KEY")
    return ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=temperatura, google_api_key=api_key)

def generar_nudge(mensaje_usuario, contexto_financiero):
    """Genera un consejo empático fundamentado en RAG y en los datos bancarios del usuario."""
    contexto_cientifico = buscar_contexto(mensaje_usuario, k=2)
    llm_creativo = inicializar_motor_ia(temperatura=0.5)
    
    prompt_nudge = ChatPromptTemplate.from_template(
        "Eres Nudge AI, un coach financiero conductual experto de una entidad bancaria.\n"
        "El usuario está a punto de realizar un gasto o tomar una decisión. Tu objetivo es prevenir la mora crediticia "
        "ayudándolo a mantenerse dentro de su presupuesto mediante un 'nudge' o anclaje conductual empático.\n\n"
        "--- DATOS DE SU CAJA DE AHORRO (EVALUACIÓN CREDITICIA) ---\n"
        "{datos_financieros}\n"
        "----------------------------------------------------------\n\n"
        "--- LITERATURA CIENTÍFICA (ECONOMÍA CONDUCTUAL) ---\n"
        "{contexto_rag}\n"
        "---------------------------------------------------\n\n"
        "Mensaje del usuario: {mensaje}\n\n"
        "Respuesta de Nudge AI (Háblale directamente, usa sus datos para contextualizar sin parecer un robot calculador, y felicítalo si tiene buena racha):"
    )
    
    cadena_nudge = prompt_nudge | llm_creativo | StrOutputParser()
    return cadena_nudge.invoke({
        "contexto_rag": contexto_cientifico, 
        "datos_financieros": contexto_financiero,
        "mensaje": mensaje_usuario
    })

def procesar_mensaje_coach(mensaje_usuario, contexto_financiero="Sin datos financieros proporcionados."):
    """Función principal que la interfaz web llamará para obtener respuestas."""
    try:
        llm_triaje = inicializar_motor_ia(temperatura=0.0).with_structured_output(TriajeFinanciero)
        prompt_triaje = ChatPromptTemplate.from_template(
            "Eres un especialista en triaje de finanzas conductuales.\n"
            "Analiza el mensaje del usuario y clasifica la intención considerando su contexto.\n\n"
            "Reglas de decisión:\n"
            "- NUDGE_REFLEXIVO: El usuario expresa intención de realizar una compra, gasto emocional, o se nota estrés.\n"
            "- EXPLORAR_CONTEXTO: El mensaje es impreciso.\n"
            "- ESCALAR_ASESOR: El usuario solicita transacciones reales.\n\n"
            "Mensaje del usuario: {mensaje_usuario}"
        )
        cadena_triaje = prompt_triaje | llm_triaje
        resultado_triaje = cadena_triaje.invoke({"mensaje_usuario": mensaje_usuario})
        
        if resultado_triaje.decision == "NUDGE_REFLEXIVO":
            return generar_nudge(mensaje_usuario, contexto_financiero)
            
        elif resultado_triaje.decision == "EXPLORAR_CONTEXTO":
            campos = ", ".join(resultado_triaje.campos_faltantes)
            return f"Para poder ayudarte mejor, ¿podrías darme un poco más de contexto? Me faltan estos detalles: **{campos}**."
            
        elif resultado_triaje.decision == "ESCALAR_ASESOR":
            return "He detectado que necesitas realizar una operación transaccional. Te estoy transfiriendo con un asesor humano seguro..."
            
    except Exception as e:
        return f"Ocurrió un error en el sistema cognitivo: {e}"