import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Cargar de forma segura las credenciales del archivo .env
load_dotenv()

def inicializar_motor_ia():
    """Configura y conecta con el modelo de lenguaje de Google Gemini."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("¡Error! No se encontró la variable GEMINI_API_KEY en el archivo .env")
    
    # Inicializamos el modelo. 
    # Usamos una temperatura baja (0.2) para que las respuestas financieras sean estables y analíticas.
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash", 
        temperature=0.2,
        google_api_key=api_key
    )
    return llm

if __name__ == "__main__":
    print("Iniciando el Agente de Tecnología Financiera Conductual...")
    try:
        # Inicializar conexión
        llm = inicializar_motor_ia()
        
        # Diseñar una prueba conceptual de salud financiera
        prompt = ChatPromptTemplate.from_template(
            "Eres un asistente de IA avanzado especializado en finanzas conductuales. "
            "El usuario tiende a realizar compras impulsivas cuando experimenta altos niveles de estrés. "
            "Proporciónale una estrategia breve, práctica y empática (un 'nudge' o estímulo positivo) "
            "para ayudarlo a pausar y reflexionar antes de gastar."
        )
        
        # Construir la cadena de ejecución (Añadimos el StrOutputParser al final)
        chain = prompt | llm | StrOutputParser()

        # Ejecutar la consulta
        print("\nEnviando consulta de prueba al modelo...")
        respuesta = chain.invoke({}) # Ahora la respuesta ya vendrá en texto limpio

        print("\n" + "="*40)
        print("RESPUESTA DEL AGENTE FINTECH:")
        print("="*40)
        print(respuesta)  
        print("="*40 + "\n")
        print("¡Conexión completada y verificada con éxito!")
        
    # ESTAS SON LAS LÍNEAS QUE FALTABAN:
    except Exception as e:
        print(f"\n Ocurrió un error durante la ejecución: {e}")