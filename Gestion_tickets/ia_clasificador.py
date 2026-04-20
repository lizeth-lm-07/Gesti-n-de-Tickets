import json
import re
from anthropic import Anthropic

client = Anthropic(api_key="")

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
- Media: afecta parcialmente pero no detiene todo
- Baja: informativo o no urgente

Ejemplos:

Ticket: "No puedo entrar a la plataforma"
Respuesta: {{"categoria": "Servicios", "prioridad": "Alta"}}

Ticket: "El maestro no vino a clase"
Respuesta: {{"categoria": "Docencia", "prioridad": "Alta"}}

Ticket: "El aire acondicionado no funciona"
Respuesta: {{"categoria": "Infraestructura", "prioridad": "Media"}}

Ticket: "Tengo duda sobre mi pago"
Respuesta: {{"categoria": "Administrativo", "prioridad": "Baja"}}

Responde ÚNICAMENTE con JSON válido, sin explicaciones.

Ticket:
"{texto}"
"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}]
    )

    texto_respuesta = response.content[0].text.strip()

    print("Respuesta IA:", texto_respuesta)

    try:
        json_texto = re.search(r'\{.*\}', texto_respuesta, re.DOTALL).group()
        resultado = json.loads(json_texto)

        print("JSON limpio:", resultado)

        return resultado

    except Exception as e:
        print("Error procesando IA:", e)
        return {"categoria": "Servicios", "prioridad": "Media"}