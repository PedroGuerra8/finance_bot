import re


CATEGORIAS = {
    "alimentacao": ["mercado", "comida", "almoço", "janta", "lanche", "alimentacao"],
    "transporte": ["uber", "99", "ônibus", "metro", "transporte"],
    "lazer": ["cinema", "bar", "show", "lazer"],
    "contas": ["luz", "agua", "internet", "aluguel", "conta"]
}

ENTRADAS = ["recebi", "entrada", "ganhei", "salario"]
SAIDAS = ["gastei", "paguei", "pago"]


def normalizar_valor(valor_str: str) -> float:
    return float(valor_str.replace(",", "."))


def identificar_categoria(texto: str) -> str:
    for categoria, palavras in CATEGORIAS.items():
        for palavra in palavras:
            if palavra in texto:
                return categoria
    return "outros"


def parse_mensagem(texto: str):
    texto = texto.lower()

    # saldo
    if texto.startswith("saldo"):
        return {"acao": "saldo"}

    # total do mês
    if texto.startswith("total"):
        categoria = identificar_categoria(texto)
        return {"acao": "total_mes", "categoria": categoria}

    # valor
    match = re.search(r"(\d+[.,]?\d*)", texto)
    if not match:
        return {"erro": "valor_nao_encontrado"}

    valor = normalizar_valor(match.group(1))

    # entrada
    if any(p in texto for p in ENTRADAS):
        descricao = texto.replace(match.group(1), "").strip()
        return {
            "acao": "entrada",
            "valor": valor,
            "descricao": descricao
        }

    # saída
    if any(p in texto for p in SAIDAS):
        categoria = identificar_categoria(texto)
        descricao = texto.replace(match.group(1), "").strip()
        return {
            "acao": "saida",
            "valor": valor,
            "categoria": categoria,
            "descricao": descricao
        }

    return {"erro": "comando_nao_reconhecido"}
