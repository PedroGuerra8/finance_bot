from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    descricao = Column(String, nullable=True)
    data = Column(DateTime, default=datetime.utcnow)
