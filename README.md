# Nudge AI - Prevención de Riesgo y Coach Conductual

> **Estado del Proyecto:** 🚀 Prototipo Funcional Avanzado (Monitoreo Preventivo)

Nudge AI es un agente de Inteligencia Artificial especializado en finanzas conductuales (*Behavioral Finance*) y gestión de riesgo crediticio. Diseñado para entidades financieras, este sistema evoluciona el modelo tradicional de evaluación crediticia al realizar un seguimiento continuo post-desembolso. 

Mediante la lectura de datos de la caja de ahorro del cliente, Nudge AI envía "nudges" (estímulos empáticos) de forma proactiva para evitar gastos impulsivos por estrés, prevenir la mora crediticia y fomentar la disciplina financiera a través de un sistema de recompensas gamificado (ej. reducción de tasas de interés).

## 🎯 Objetivos del Proyecto

* **Prevención de Mora Crediticia:** Monitorear la velocidad de gasto mensual para intervenir conductualmente antes de que el cliente se quede sin liquidez para su cuota.
* **Intervención Conductual:** Detectar momentos de fricción emocional y proporcionar estrategias de pausa reflexiva fundamentadas en la literatura científica.
* **Sistema de Recompensas (Contratos de Ulises):** Fomentar el buen comportamiento de pago mediante metas gamificadas y beneficios financieros tangibles.
* **Innovación FinTech:** Aplicar modelos de lenguaje de vanguardia en el análisis de riesgo y comportamiento dentro del ecosistema bancario boliviano y regional.

## 🛠️ Tecnologías y Arquitectura

Este proyecto está construido con una **Arquitectura Multi-Agente** con memoria aumentada y análisis de datos en tiempo real:

* **Interfaz y Dashboard:** Streamlit (Panel visual de perfil crediticio y chat interactivo).
* **Lenguaje:** Python 3.10+
* **Orquestación:** LangChain (Cadenas, Output Parsers y Enrutamiento Dinámico).
* **Motor de IA:** Google Gemini 3.5 Flash (Generación empática y triaje cognitivo).
* **Memoria RAG:** FAISS + HuggingFace (`all-MiniLM-L6-v2`) para la integración estricta de bibliografía conductual (Kahneman, Thaler).
* **Validación Estructural:** Pydantic (Garantía de formato JSON).
* **Seguridad:** `python-dotenv` para gestión de credenciales.

## 🚀 Roadmap del Proyecto

- [x] Conexión segura con el motor LLM (Gemini).
- [x] Implementación de "Nudges" conductuales mediante System Prompts.
- [x] Agente de Triaje Cognitivo (Clasificador de intenciones).
- [x] Implementación de memoria RAG para lectura de bibliografía conductual.
- [x] Desarrollo de Interfaz de Usuario interactiva (Streamlit).
- [x] **NUEVO:** Integración de Dashboard de Evaluación Crediticia (Simulación de Caja de Ahorro).
- [x] **NUEVO:** Lógica de monitoreo preventivo de mora y sistema de recompensas.

---
*Desarrollado con un enfoque científico y tecnológico para la modernización financiera desde Bolivia.*