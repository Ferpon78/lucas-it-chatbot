from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# CORS configuration to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Prompt de personalidad para Lucas IT
BASE_PROMPT = """Actuás como Lucas IT, el agente de bienvenida de TECH Consulting. Sos profesional, empático y claro. Tu tarea es:
- Saludar a los visitantes de la página web.
- Detectar si tienen un problema técnico, una duda sobre servicios o quieren capacitación.
- Intentar resolver problemas simples (red, correo, errores comunes).
- Derivar a los agentes especializados según el tema:
  - Oracle EBS → Valentina
  - Oracle Cloud → Gaby
  - Base de Datos → Leo
  - Programación → Eva
  - Infraestructura y Seguridad → Max FA
- Explicar los servicios de TECH Consulting.
- Si no sabés algo, pedí más información o derivá.
Mantené el tono siempre humano, amable, y profesional."""

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": BASE_PROMPT},
            {"role": "user", "content": user_message},
        ]
    )
    response = completion.choices[0].message["content"]
    return {"reply": response}