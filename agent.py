import os
from dotenv import load_dotenv
from typing import Literal, List
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# 1. Cargar credenciales
load_dotenv()

# 2. Definir la Estructura de Salida (El JSON esperado) usando Pydantic
class TriajeFinanciero(BaseModel):
    decision: Literal["NUDGE_REFLEXIVO", "EXPLORAR_CONTEXTO", "ESCALAR_ASESOR"] = Field(
        description="La acción que debe tomar el sistema basándose en la intención del usuario."
    )
    urgencia: Literal["BAJA", "MEDIANA", "ALTA"] = Field(
        description="Nivel de urgencia financiera o emocional."
    )
    campos_faltantes: List[str] = Field(
        default_factory=list,
        description="Si la decisión es EXPLORAR_CONTEXTO, lista qué información falta (ej. 'estado_emocional', 'monto_del_gasto')."
    )

def inicializar_motor_ia():
    """Configura y conecta con Google Gemini."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("¡Error! No se encontró la variable GEMINI_API_KEY")
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash", 
        temperature=0.0, # Temperatura 0 para tareas de clasificación lógica (Triaje)
        google_api_key=api_key
    )
    
    # ¡Magia de LangChain! Obligamos al LLM a respetar la estructura de Pydantic
    llm_estructurado = llm.with_structured_output(TriajeFinanciero)
    return llm_estructurado

if __name__ == "__main__":
    print("Iniciando el Enrutador de Nudge AI...")
    try:
        # Inicializar el modelo estructurado
        llm_triaje = inicializar_motor_ia()
        
        # Diseñar el Prompt del Triaje Conductual
        prompt_triaje = ChatPromptTemplate.from_template(
            """Eres un especialista en triaje de finanzas conductuales.
            Analiza el mensaje del usuario y clasifica la intención.
            
            Reglas de decisión:
            - NUDGE_REFLEXIVO: El usuario expresa intención de realizar una compra impulsiva, gasto innecesario o decisiones financieras basadas en emociones.
            - EXPLORAR_CONTEXTO: El mensaje es impreciso o falta contexto para entender su situación financiera o emocional.
            - ESCALAR_ASESOR: El usuario solicita transacciones bancarias reales, revisión de contratos, cancelación de tarjetas, o asesoría de inversiones complejas.
            
            Mensaje del usuario: {mensaje_usuario}
            """
        )
        
        # Construir la cadena
        cadena_triaje = prompt_triaje | llm_triaje

        # --- PRUEBA 1: Compra Impulsiva ---
        mensaje_1 = "Estoy muy estresado por el trabajo, creo que me merezco comprar esa consola de videojuegos de $500 dólares ahora mismo."
        print(f"\nProcesando Mensaje: '{mensaje_1}'")
        resultado_1 = cadena_triaje.invoke({"mensaje_usuario": mensaje_1})
        print(f"Decisión del Agente: {resultado_1.decision} (Urgencia: {resultado_1.urgencia})")

        # --- PRUEBA 2: Transacción pura ---
        mensaje_2 = "Necesito que bloqueen mi tarjeta de crédito porque la perdí."
        print(f"\nProcesando Mensaje: '{mensaje_2}'")
        resultado_2 = cadena_triaje.invoke({"mensaje_usuario": mensaje_2})
        print(f"Decisión del Agente: {resultado_2.decision} (Urgencia: {resultado_2.urgencia})")
        print("\n¡Triaje completado con éxito!")
        
    except Exception as e:
        print(f"\n Ocurrió un error durante la ejecución: {e}")