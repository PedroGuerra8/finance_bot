from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI()

class WebhookPayload(BaseModel):
    mensagem: str | None = None

def extrair_gasto(texto: str):
    # procura número inteiro ou decimal (23 ou 23,50 ou 23.50)
    match = re.search(r'(\d+[.,]?\d*)', texto)

    if not match:
        return None, None

    valor_str = match.group(1).replace(',', '.')
    valor = float(valor_str)

    descricao = texto.replace(match.group(1), '').strip()

    return descricao, valor

@app.post("/webhook")
async def webhook(payload: WebhookPayload):
    texto = payload.mensagem or ""

    descricao, valor = extrair_gasto(texto)

    if valor is None:
        return {
            "resposta": "❌ Não consegui identificar o valor. Ex: mercado 180"
        }

    return {
        "resposta": f"✅ Gasto registrado: {descricao.title()} – R$ {valor:.2f}"
    }
