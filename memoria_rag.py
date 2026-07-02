import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Cargar variables de entorno
load_dotenv()

def construir_base_conocimiento():
    print("Iniciando lectura de los libros PDF en la carpeta 'data/'. Esto puede tomar un minuto...")
    
    # 1. Cargar TODOS los PDFs del directorio
    ruta_directorio = "./data"
    if not os.path.exists(ruta_directorio):
        raise FileNotFoundError(f"No se encontró la carpeta en {ruta_directorio}")
        
    loader = PyPDFDirectoryLoader(ruta_directorio)
    documentos = loader.load()
    print(f"Se han cargado {len(documentos)} páginas en total de los libros.")
    
    # 2. Dividir el texto en fragmentos
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500, 
        chunk_overlap=200 
    )
    fragmentos = text_splitter.split_documents(documentos)
    print(f"Los libros se han dividido en {len(fragmentos)} fragmentos procesables.")
    
    # 3. Crear Embeddings LOCALES (Rápidos, gratuitos y sin errores 404)
    print("Descargando e inicializando modelo matemático local (all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 4. Almacenar en FAISS
    print("Creando los vectores matemáticos y guardando en FAISS...")
    vectorstore = FAISS.from_documents(fragmentos, embeddings)
    
    # 5. Guardar la base de datos localmente
    vectorstore.save_local("faiss_index")
    print("¡Base de datos vectorial construida y guardada en local (faiss_index/) con éxito!")
    
    return vectorstore

def buscar_contexto(consulta, k=3):
    """Busca en la base de datos vectorial los 3 fragmentos más relevantes de los libros."""
    # Instanciar el mismo modelo local para la búsqueda
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Cargar la base de datos pre-construida
    vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    
    # Realizar búsqueda de similitud matemática
    resultados = vectorstore.similarity_search(consulta, k=k)
    
    # Unir los fragmentos encontrados
    contexto_unido = "\n\n".join([doc.page_content for doc in resultados])
    return contexto_unido

if __name__ == "__main__":
    # Fase 1: Construir la base de datos
    construir_base_conocimiento()
    
    # Fase 2: Prueba de búsqueda experta
    print("\n--- PRUEBA DE MEMORIA RAG CON LOS LIBROS ---")
    pregunta_prueba = "¿Qué es el Sistema 1 y cómo afecta a las decisiones financieras?"
    print(f"Consulta al sistema: {pregunta_prueba}\n")
    
    contexto_recuperado = buscar_contexto(pregunta_prueba)
    print("Conocimiento recuperado de los libros:")
    print("="*60)
    print(contexto_recuperado)
    print("="*60)