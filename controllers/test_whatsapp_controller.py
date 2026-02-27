from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from services.transacoes_service import (
    registrar_entrada,
    registrar_saida,
    calcular_saldo
)
from services.parser_service import parse_mensagem

router = APIRouter()


@router.post("/whatsapp-test")
def whatsapp_simulado(
    payload: dict,
    db: Session = Depends(get_db)
):
    texto = payload.get("message", "").lower()
    numero = payload.get("from", "5511999999999")

    resultado = parse_mensagem(texto)

    if resultado.get("acao") == "entrada":
        saldo = registrar_entrada(
            db,
            resultado["valor"],
            resultado.get("descricao")
        )
        resposta = f"✅ Entrada registrada. Saldo: {saldo}"

    elif resultado.get("acao") == "saida":
        saldo = registrar_saida(
            db,
            resultado["valor"],
            resultado["categoria"],
            resultado.get("descricao")
        )
        resposta = f"💸 Gasto registrado ({resultado['categoria']}). Saldo: {saldo}"

    elif resultado.get("acao") == "saldo":
        saldo = calcular_saldo(db)
        resposta = f"💰 Seu saldo atual é: {saldo}"

    elif resultado.get("acao") == "total_mes":
        resposta = "🚧 Total do mês em construção 😄"

    else:
        resposta = "❌ Não entendi. Ex: gastei 50 mercado, recebi 3000 salario"

    return {
        "from": numero,
        "response": resposta
    }
