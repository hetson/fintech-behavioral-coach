import os
from dotenv import load_dotenv
from typing import Literal, List
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Cargar credenciales
load_dotenv()

# 2. Definir la Estructura de Salida para el Triaje
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
    """Configura y conecta con Google Gemini. Permite ajustar la temperatura dinámicamente."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("¡Error! No se encontró la variable GEMINI_API_KEY")
    
    return ChatGoogleGenerativeAI(
        model="gemini-3.5-flash", 
        temperature=temperatura,
        google_api_key=api_key
    )

def generar_nudge(mensaje_usuario):
    """Genera un consejo empático cuando se detecta un gasto impulsivo."""
    print("\n[Activando Motor de Coaching Conductual...]")
    
    # Instanciamos un modelo diferente: temperatura 0.5 para mayor empatía y creatividad
    llm_creativo = inicializar_motor_ia(temperatura=0.5)
    
    prompt_nudge = ChatPromptTemplate.from_template(
        "Eres Nudge AI, un coach financiero conductual. "
        "El usuario está a punto de realizar un gasto impulsivo debido a una emoción. "
        "Tu objetivo es brindarle una respuesta breve, muy empática, sin juzgarlo, "
        "y ofrecerle una alternativa o un anclaje conductual (ej. la regla de las 24 horas, o calcular las horas de trabajo que cuesta). "
        "Háblale de tú a tú, con un tono amable y profesional.\n\n"
        "Mensaje del usuario: {mensaje}\n\n"
        "Respuesta del Coach:"
    )
    
    # Usamos StrOutputParser porque aquí sí queremos texto legible, no JSON
    cadena_nudge = prompt_nudge | llm_creativo | StrOutputParser()
    return cadena_nudge.invoke({"mensaje": mensaje_usuario})

if __name__ == "__main__":
    print("Iniciando el Enrutador de Nudge AI...")
    try:
        # Inicializar el modelo estructurado para el triaje (temperatura 0.0)
        llm_triaje = inicializar_motor_ia(temperatura=0.0).with_structured_output(TriajeFinanciero)
        
        prompt_triaje = ChatPromptTemplate.from_template(
            "Eres un especialista en triaje de finanzas conductuales.\n"
            "Analiza el mensaje del usuario y clasifica la intención.\n\n"
            "Reglas de decisión:\n"
            "- NUDGE_REFLEXIVO: El usuario expresa intención de realizar una compra impulsiva, gasto emocional o por estrés.\n"
            "- EXPLORAR_CONTEXTO: El mensaje es impreciso o le falta contexto.\n"
            "- ESCALAR_ASESOR: El usuario solicita transacciones o trámites bancarios reales.\n\n"
            "Mensaje del usuario: {mensaje_usuario}"
        )
        
        cadena_triaje = prompt_triaje | llm_triaje

        # --- PRUEBA CONTEXTUALIZADA DE ESTRÉS ---
        mensaje_prueba = "Tuve una semana pesadísima, quiero irme a gastar todos mis ahorros de fiesta y compras por el centro de Cochabamba para olvidarme de todo."
        
        print(f"\nUsuario: '{mensaje_prueba}'")
        print("Analizando intención...")
        
        # 1. El Triaje clasifica el mensaje
        resultado_triaje = cadena_triaje.invoke({"mensaje_usuario": mensaje_prueba})
        print(f"Decisión del Triaje: {resultado_triaje.decision} (Urgencia: {resultado_triaje.urgencia})")

        # 2. Lógica de Enrutamiento Condicional
        if resultado_triaje.decision == "NUDGE_REFLEXIVO":
            # Si es impulsivo, generamos el consejo
            consejo = generar_nudge(mensaje_prueba)
            print("\n" + "="*60)
            print("🧠 RESPUESTA DE NUDGE AI:")
            print("="*60)
            print(consejo)
            print("="*60)
            
        elif resultado_triaje.decision == "EXPLORAR_CONTEXTO":
            print("\nSistema: Por favor, cuéntame un poco más. Me faltan estos detalles:", resultado_triaje.campos_faltantes)
            
        elif resultado_triaje.decision == "ESCALAR_ASESOR":
            print("\nSistema: Esta es una solicitud transaccional. Transfiriendo a un asesor humano...")
        
    except Exception as e:
        print(f"\n Ocurrió un error durante la ejecución: {e}")