from anthropic import Anthropic

client = Anthropic(api_key="tu_key")

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=50,
    messages=[{"role": "user", "content": "Di hola"}]
)

print(response.content[0].text)