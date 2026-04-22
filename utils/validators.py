def validar_registro(registro: dict) -> bool:
    campos = ["data", "valor", "descricao", "categoria", "tipo"]
    return all(campo in registro for campo in campos)
