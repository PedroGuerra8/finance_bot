from fastapi import FastAPI
from pydantic import BaseModel
import re
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = FastAPI()

# MongoDB
client = MongoClient(os.getenv("MONGO_URL"))
db = client[os.getenv("DB_NAME")]
gastos_collection = db["gastos"]

# -----------------------
# MODELO
# -----------------------

class WebhookPayload(BaseModel):
    mensagem: str | None = None

# -----------------------
# CONFIGURAÇÕES
# -----------------------

CATEGORIAS = ["lazer", "alimentacao", "transporte", "contas"]
PALAVRAS_ENTRADA = ["pix", "salario", "salário", "entrada", "recebi"]
PALAVRAS_DELETE = ["apagar", "deletar", "remover"]
PALAVRAS_SALDO = ["saldo", "quanto tenho", "quanto sobrou"]
PALAVRAS_TOTAL_MES = ["total do mes", "total do mês", "gastei no mes"]

# -----------------------
# FUNÇÕES AUXILIARES
# -----------------------

def extrair_valor(texto: str):
    match = re.search(r'(\d+[.,]?\d*)', texto)
    if not match:
        return None
    return float(match.group(1).replace(",", "."))

def identificar_tipo(texto: str):
    texto = texto.lower()
    for palavra in PALAVRAS_ENTRADA:
        if palavra in texto:
            return "entrada"
    return "saida"

def identificar_categoria(texto: str):
    texto = texto.lower()
    for categoria in CATEGORIAS:
        if categoria in texto:
            return categoria
    return "outros"

def limpar_descricao(texto: str, valor: float):
    return texto.replace(str(valor), "").strip()

def is_delete(texto: str):
    return any(p in texto.lower() for p in PALAVRAS_DELETE)

def is_saldo(texto: str):
    return any(p in texto.lower() for p in PALAVRAS_SALDO)

def is_total_mes(texto: str):
    return any(p in texto.lower() for p in PALAVRAS_TOTAL_MES)

def calcular_saldo():
    entradas = 0
    saidas = 0

    for g in gastos_collection.find():
        if g["tipo"] == "entrada":
            entradas += g["valor"]
        else:
            saidas += g["valor"]

    return entradas, saidas, entradas - saidas

def total_mes_atual():
    agora = datetime.now()
    total = 0

    for g in gastos_collection.find({
        "tipo": "saida",
        "data": {
            "$gte": datetime(agora.year, agora.month, 1)
        }
    }):
        total += g["valor"]

    return total

# -----------------------
# WEBHOOK (WHATSAPP)
# -----------------------

@app.post("/webhook")
async def webhook(payload: WebhookPayload):
    texto = payload.mensagem or ""

    # DELETE
    if is_delete(texto):
        ultimo = gastos_collection.find_one(sort=[("data", -1)])

        if not ultimo:
            return {"resposta": "⚠️ Não há registros para apagar."}

        gastos_collection.delete_one({"_id": ultimo["_id"]})

        return {
            "resposta": (
                f"🗑️ Última movimentação apagada:\n"
                f"{ultimo['descricao']} – R$ {ultimo['valor']:.2f}"
            )
        }

    # SALDO
    if is_saldo(texto):
        entradas, saidas, saldo = calcular_saldo()

        return {
            "resposta": (
                f"📊 Saldo atual\n"
                f"💰 Entradas: R$ {entradas:.2f}\n"
                f"💸 Saídas: R$ {saidas:.2f}\n"
                f"🧾 Saldo: R$ {saldo:.2f}"
            )
        }

    # TOTAL DO MÊS
    if is_total_mes(texto):
        total = total_mes_atual()
        return {
            "resposta": f"📆 Total gasto neste mês: R$ {total:.2f}"
        }

    # REGISTRO
    valor = extrair_valor(texto)
    if valor is None:
        return {"resposta": "❌ Não encontrei valor. Ex: mercado 180"}

    tipo = identificar_tipo(texto)
    categoria = identificar_categoria(texto)
    descricao = limpar_descricao(texto, valor)

    gasto = {
        "tipo": tipo,
        "descricao": descricao,
        "categoria": categoria,
        "valor": valor,
        "data": datetime.now()
    }

    gastos_collection.insert_one(gasto)

    emoji = "💰" if tipo == "entrada" else "💸"

    return {
        "resposta": (
            f"{emoji} {tipo.upper()} registrada!\n"
            f"📌 {descricao}\n"
            f"🏷️ {categoria}\n"
            f"💵 R$ {valor:.2f}"
        )
    }

# -----------------------
# GET - LISTAR (DEBUG)
# -----------------------

@app.get("/gastos")
def listar_gastos():
    resultado = []

    for g in gastos_collection.find().sort("data", -1):
        resultado.append({
            "id": str(g["_id"]),
            "tipo": g["tipo"],
            "descricao": g["descricao"],
            "categoria": g["categoria"],
            "valor": g["valor"],
            "data": g["data"]
        })

    return resultado
