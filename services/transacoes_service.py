from sqlalchemy.orm import Session
from models import Transacao


def registrar_entrada(db: Session, valor: float, descricao: str | None):
    transacao = Transacao(
        tipo="entrada",
        valor=valor,
        descricao=descricao
    )

    db.add(transacao)
    db.commit()

    return calcular_saldo(db)


def registrar_alimentacao(db: Session, valor: float, descricao: str | None):
    transacao = Transacao(
        tipo="alimentacao",
        valor=valor,
        descricao=descricao
    )

    db.add(transacao)
    db.commit()

    return calcular_saldo(db)


def calcular_saldo(db: Session):
    entradas = (
        db.query(Transacao)
        .filter(Transacao.tipo == "entrada")
        .all()
    )

    saidas = (
        db.query(Transacao)
        .filter(Transacao.tipo != "entrada")
        .all()
    )

    return sum(t.valor for t in entradas) - sum(t.valor for t in saidas)
