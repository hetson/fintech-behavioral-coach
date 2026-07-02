# Nudge AI - Coach Financiero Conductual

> **Estado del Proyecto:** 🚧 En desarrollo activo

Nudge AI es un agente de Inteligencia Artificial especializado en finanzas conductuales (*Behavioral Finance*). A diferencia de las aplicaciones bancarias transaccionales estándar, este proyecto está diseñado para funcionar como un coach financiero personal, analizando patrones y enviando "nudges" (estímulos positivos) empáticos en tiempo real para ayudar a los usuarios a evitar gastos impulsivos por estrés y mejorar su toma de decisiones financieras.

## 🎯 Objetivos del Proyecto

* **Intervención Conductual:** Detectar momentos de fricción emocional y proporcionar estrategias de pausa reflexiva.
* **Educación Financiera:** Integrar conceptos de economía conductual para transformar los hábitos de gasto.
* **Innovación FinTech:** Aplicar modelos de lenguaje de vanguardia en el análisis de riesgo y comportamiento dentro del ecosistema financiero.

## 🛠️ Tecnologías y Arquitectura

Este proyecto está construido con una **Arquitectura Multi-Agente** con memoria aumentada:

* **Lenguaje:** Python 3.10+
* **Orquestación:** LangChain (Cadenas, Output Parsers y Enrutamiento Dinámico)
* **Motor de IA:** Google Gemini 3.5 Flash (Generación de texto y triaje)
* **Memoria RAG:** FAISS (Base de datos vectorial) + HuggingFace (`all-MiniLM-L6-v2` para Embeddings locales de alto rendimiento).
* **Validación Estructural:** Pydantic (Para garantizar el formato JSON exacto)
* **Seguridad:** `python-dotenv` para gestión de credenciales.

## 🚀 Próximos Pasos (Roadmap)

- [x] Conexión segura con el motor LLM (Gemini).
- [x] Implementación de "Nudges" conductuales.
- [x] Agente de Triaje Cognitivo (Clasificador de intenciones).
- [x] Enrutamiento Multi-Agente.
- [x] Implementación de memoria RAG para lectura de bibliografía conductual (Kahneman, Thaler).
- [x] Integración del Agente Principal con la Memoria RAG.
- [ ] Desarrollo de Interfaz de Usuario interactiva (Streamlit).

---
*Desarrollado con enfoque en la innovación financiera desde Bolivia.*