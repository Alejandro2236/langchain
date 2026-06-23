import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from schema import FormularioIncidente, TicketAnalizado
from database import guardar_en_postgres
from mailer import enviar_correo_alta_prioridad

# Cargar variables de entorno
load_dotenv()

# Inicializar FastAPI (Sustituye al Webhook/Form Trigger de n8n)
app = FastAPI(title="SmartTicket Replicado en LangChain")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)
llm_estructurado = llm.with_structured_output(TicketAnalizado)

prompt = ChatPromptTemplate.from_messages([
    ("system", """Eres un Ingeniero de Soporte Nivel 3 en una corporación multinacional. Tu tarea es analizar de forma rigurosa la descripción del incidente.

**[PASO 1: VALIDACIÓN DE SEGURIDAD Y SENTIDO]**
Antes de clasificar, evalúa si el texto de la descripción tiene sentido, contiene suficiente contexto técnico o está relacionado con la empresa. Si la descripción está vacía, contiene solo caracteres aleatorios (ej. "asdasd"), saludos simples sin contexto (ej. "hola"), o temas completamente ajenos a la tecnología empresarial, debes marcar la categoria como 'No Clasificable / Inválido' y la criticidad en 'N/A'.

**[PASO 2: ASIGNACIÓN DE CRITICIDAD VALIDADA]**
- Alta: Si el problema detiene la operación de un departamento entero.
- Media: Si afecta el trabajo diario de un equipo pero hay alternativas temporales.
- Baja: Si es un problema individual o estético.

**[PASO 3: DETALLE TÉCNICO]**
- Resumen: Máximo 15 palabras. Si es inválido, usa: 'Entrada de usuario no procesable'.
- Solucion: Pasos iniciales de mitigación. Si es inválido, usa exactamente: 'Rechazado: El reporte no contiene un incidente de TI válido.'"""),
    ("human", "Departamento: {departamento}\nDescripción del Incidente: {descripcion}")
])

chain = prompt | llm_estructurado

@app.post("/procesar-ticket")
async def procesar_ticket(datos_form: FormularioIncidente):
    print(f"\n[Form Trigger] Recibido reporte de: {datos_form.empleado}")
    
    resultado_ia: TicketAnalizado = chain.invoke({
        "departamento": datos_form.departamento,
        "descripcion": datos_form.descripcion
    })
    
    guardar_en_postgres(datos_form, resultado_ia)
    
    if resultado_ia.criticidad == "Alta":
        enviar_correo_alta_prioridad(datos_form, resultado_ia)
    else:
        print(f"[Switch] Criticidad '{resultado_ia.criticidad}'. No requiere disparo de Email.")
        
    return {
        "status": "Procesado",
        "entrada_recibida": datos_form,
        "analisis_ia": resultado_ia
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)