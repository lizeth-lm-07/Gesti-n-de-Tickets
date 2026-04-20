import json
from anthropic import Anthropic

client = Anthropic(api_key="TU_API_KEY")

def clasificar_ticket(texto):
    prompt = f"""
Clasifica este ticket de una escuela:

Categorías:
- Infraestructura
- Servicios
- Docencia
- Administrativo

Prioridades:
- Alta
- Media
- Baja

Reglas:
- Alta: bloquea clases o acceso
- Media: afecta pero no detiene
- Baja: informativo

Ticket:
"{texto}"

Responde SOLO en JSON:
{{"categoria": "...", "prioridad": "..."}}
"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}]
    )

    texto_respuesta = response.content[0].text.strip()

    try:
        return json.loads(texto_respuesta)
    except:
        return {"categoria": "Servicios", "prioridad": "Media"}