import csv
import os
from datetime import datetime, date
from typing import List, Dict, Optional

# ======================
# CONFIGURAÇÕES
# ======================
BASE_DIR = "database"
ARQUIVO = os.path.join(BASE_DIR, "registros.csv")

CAMPOS = [
    "usuario_id",
    "data",
    "descricao",
    "observacao",
    "valor",
    "categoria",
    "tipo"
]

DATA_FORMAT = "%Y-%m-%d"


# ======================
# UTILITÁRIOS INTERNOS
# ======================
def _garantir_diretorio():
    os.makedirs(BASE_DIR, exist_ok=True)


def _normalizar_registro(registro: Dict) -> Dict:
    """
    Garante que o registro tenha todos os campos
    e tipos corretos antes de salvar
    """
    registro_padrao = {campo: "" for campo in CAMPOS}
    registro_padrao.update(registro)

    # Normaliza data
    if isinstance(registro_padrao["data"], (datetime, date)):
        registro_padrao["data"] = registro_padrao["data"].strftime(DATA_FORMAT)

    # Normaliza valor
    try:
        registro_padrao["valor"] = float(registro_padrao["valor"])
    except (TypeError, ValueError):
        registro_padrao["valor"] = 0.0

    # Normaliza tipo
    if registro_padrao["tipo"]:
        registro_padrao["tipo"] = registro_padrao["tipo"].strip().capitalize()

    return registro_padrao


def _converter_registro(row: Dict) -> Optional[Dict]:
    """
    Converte dados do CSV (string) para tipos corretos
    """
    try:
        row["valor"] = float(row["valor"])
        row["data"] = datetime.strptime(row["data"], DATA_FORMAT)
        return row
    except (ValueError, KeyError):
        return None


# ======================
# SALVAR REGISTRO
# ======================
def salvar_registro(registro: Dict) -> None:
    """
    Salva um registro financeiro no CSV
    """
    _garantir_diretorio()
    registro = _normalizar_registro(registro)

    arquivo_existe = os.path.exists(ARQUIVO)

    with open(ARQUIVO, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CAMPOS)

        if not arquivo_existe:
            writer.writeheader()

        writer.writerow(registro)


# ======================
# CARREGAR DADOS
# ======================
def carregar_dados(usuario_id: Optional[str] = None) -> List[Dict]:
    """
    Carrega registros financeiros.
    Se usuario_id for informado, filtra por usuário.
    """
    if not os.path.exists(ARQUIVO):
        return []

    registros: List[Dict] = []

    with open(ARQUIVO, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            registro = _converter_registro(row)
            if registro:
                registros.append(registro)

    if usuario_id:
        registros = [r for r in registros if r["usuario_id"] == usuario_id]

    return registros


# ======================
# DELETAR REGISTRO
# ======================
def deletar_registro(index: int, usuario_id: Optional[str] = None) -> bool:
    """
    Remove um registro pelo índice (respeitando o usuário)
    """
    registros = carregar_dados()

    if usuario_id:
        registros_usuario = [r for r in registros if r["usuario_id"] == usuario_id]
    else:
        registros_usuario = registros

    if index < 0 or index >= len(registros_usuario):
        return False

    registro_remover = registros_usuario[index]
    registros.remove(registro_remover)

    _garantir_diretorio()

    with open(ARQUIVO, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CAMPOS)
        writer.writeheader()

        for r in registros:
            writer.writerow({
                **r,
                "data": r["data"].strftime(DATA_FORMAT)
            })

    return True
