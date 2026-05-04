import json
import re
import os
from anthropic import Anthropic
from dotenv import load_dotenv  

load_dotenv()  # 👈 

print("API KEY:", os.getenv("ANTHROPIC_API_KEY"))

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
# Si quieres rápido (NO recomendado):
# client = Anthropic(api_key="TU_API_KEY")


def clasificar_ticket(texto):
    prompt = f"""
Eres un sistema experto en clasificación de tickets escolares.

Clasifica el ticket en:

Categorías:
- Infraestructura: problemas físicos (salones, luz, aire, etc.)
- Servicios: plataforma, internet, sistemas
- Docencia: profesores, clases, enseñanza
- Administrativo: pagos, inscripciones, trámites

Prioridades:
- Alta: afecta directamente clases o impide el aprendizaje
- Media: afecta parcialmente
- Baja: no urgente

Además, sugiere una acción recomendada clara y breve.

Ejemplos:

Ticket: "El maestro no vino a clase"
Respuesta: {{"categoria": "Docencia", "prioridad": "Alta", "accion": "Contactar al docente y asignar reemplazo inmediato"}}

Ticket: "No puedo entrar a la plataforma"
Respuesta: {{"categoria": "Servicios", "prioridad": "Alta", "accion": "Revisar credenciales y sistema de acceso"}}

Ticket: "El aire no funciona"
Respuesta: {{"categoria": "Infraestructura", "prioridad": "Media", "accion": "Reportar a mantenimiento"}}

Ticket: "Tengo duda sobre mi pago"
Respuesta: {{"categoria": "Administrativo", "prioridad": "Baja", "accion": "Canalizar al área administrativa"}}

Responde ÚNICAMENTE con JSON válido, sin texto adicional.

Ticket:
"{texto}"
"""

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}]
        )

        texto_respuesta = response.content[0].text.strip()

        print("Respuesta IA:", texto_respuesta)

        json_texto = re.search(r'\{.*\}', texto_respuesta, re.DOTALL).group()
        resultado = json.loads(json_texto)

        print("JSON limpio:", resultado)

        return resultado

    except Exception as e:
        print("Error IA:", e)

        texto_lower = texto.lower()

        if "maestro" in texto_lower or "clase" in texto_lower:
            return {
                "categoria": "Docencia",
                "prioridad": "Alta",
                "accion": "Revisar situación del docente"
            }

        if "plataforma" in texto_lower or "login" in texto_lower:
            return {
                "categoria": "Servicios",
                "prioridad": "Alta",
                "accion": "Revisar sistema de acceso"
            }

        return {
            "categoria": "Servicios",
            "prioridad": "Media",
            "accion": "Revisar el ticket manualmente"
        }
    