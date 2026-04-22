from collections import defaultdict
from datetime import datetime, date


# ======================
# FUNÇÕES INTERNAS
# ======================
def _to_float(valor):
    try:
        return float(valor)
    except (TypeError, ValueError):
        return 0.0


def _parse_data(data):
    if isinstance(data, (datetime, date)):
        return data
    try:
        return datetime.strptime(str(data), "%Y-%m-%d")
    except Exception:
        return None


def _tipo_normalizado(tipo):
    if not tipo:
        return ""
    return tipo.strip().lower()


# ======================
# MÉTRICAS PRINCIPAIS
# ======================
def calcular_entradas(registros):
    """
    Soma apenas registros do tipo Entrada
    """
    return sum(
        _to_float(r.get("valor"))
        for r in registros
        if _tipo_normalizado(r.get("tipo")) == "entrada"
    )


def calcular_saidas(registros):
    """
    Soma apenas registros do tipo Saída
    """
    return sum(
        _to_float(r.get("valor"))
        for r in registros
        if _tipo_normalizado(r.get("tipo")) == "saída"
        or _tipo_normalizado(r.get("tipo")) == "saida"
    )


def calcular_saldo(registros):
    """
    Entradas - Saídas
    """
    entradas = calcular_entradas(registros)
    saidas = calcular_saidas(registros)
    return entradas - saidas


# ======================
# AGRUPAMENTOS
# ======================
def gastos_por_categoria(registros):
    """
    Agrupa apenas SAÍDAS por categoria
    """
    categorias = defaultdict(float)

    for r in registros:
        if _tipo_normalizado(r.get("tipo")) in ("saída", "saida"):
            categoria = r.get("categoria", "Outros")
            categorias[categoria] += _to_float(r.get("valor"))

    return dict(categorias)


# ======================
# FILTROS
# ======================
def filtrar_por_mes(registros, ano, mes):
    """
    Filtra registros por ano e mês
    """
    filtrados = []

    for r in registros:
        data = _parse_data(r.get("data"))
        if not data:
            continue

        if data.year == ano and data.month == mes:
            filtrados.append(r)

    return filtrados


def filtrar_saidas(registros):
    """
    Retorna apenas registros do tipo Saída
    """
    return [
        r for r in registros
        if _tipo_normalizado(r.get("tipo")) in ("saída", "saida")
    ]
