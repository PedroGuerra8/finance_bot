from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from services.transacoes_service import (
    registrar_entrada,
    registrar_saida,
    calcular_saldo
)
from services.whatsapp_service import enviar_mensagem

router = APIRouter()


@router.post("/webhook")
async def receber_mensagem(
    request: Request,
    db: Session = Depends(get_db)
):
    body = await request.json()

    try:
        mensagem = body["entry"][0]["changes"][0]["value"]["messages"][0]
    except (KeyError, IndexError):
        return {"status": "ignorado"}

    texto = mensagem["text"]["body"].lower()
    numero = mensagem["from"]

    if texto.startswith("entrada"):
        partes = texto.split()
        valor = float(partes[1])
        descricao = " ".join(partes[2:]) if len(partes) > 2 else None
        saldo = registrar_entrada(db, valor, descricao)
        resposta = f"✅ Entrada registrada. Saldo atual: {saldo}"

    elif texto.startswith("alimentacao"):
        partes = texto.split()
        valor = float(partes[1])
        descricao = " ".join(partes[2:]) if len(partes) > 2 else None
        saldo = registrar_saida(db, valor, descricao)
        resposta = f"🍽️ Alimentação registrada. Saldo atual: {saldo}"

    elif texto.startswith("saldo"):
        saldo = calcular_saldo(db)
        resposta = f"💰 Seu saldo atual é: {saldo}"

    else:
        resposta = "❌ Comando não reconhecido.\nUse: entrada, alimentacao ou saldo"

    enviar_mensagem(numero, resposta)

    return {"status": "ok"}
