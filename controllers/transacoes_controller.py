from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import get_db
from services.transacoes_service import (
    registrar_entrada,
    registrar_alimentacao,
    calcular_saldo
)

router = APIRouter()


@router.post("/mensagem")
def processar_mensagem(
    payload: dict,
    db: Session = Depends(get_db)
):
    mensagem = payload.get("message", "").lower()

    if mensagem.startswith("entrada"):
        partes = mensagem.split()
        valor = float(partes[1])
        descricao = " ".join(partes[2:]) if len(partes) > 2 else None
        saldo = registrar_entrada(db, valor, descricao)
        return {"saldo": saldo}

    if mensagem.startswith("alimentacao"):
        partes = mensagem.split()
        valor = float(partes[1])
        descricao = " ".join(partes[2:]) if len(partes) > 2 else None
        saldo = registrar_alimentacao(db, valor, descricao)
        return {"saldo": saldo}

    if mensagem.startswith("saldo"):
        return {"saldo": calcular_saldo(db)}

    return {"erro": "Comando não reconhecido"}
