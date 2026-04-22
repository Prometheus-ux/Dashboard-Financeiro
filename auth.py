# auth.py

def autenticar(usuario: str, senha: str) -> bool:
    """
    Autenticação simples (MVP).
    Retorna True se os dados forem válidos.
    """

    # -------- Validação básica --------
    if not usuario or not senha:
        return False

    if len(usuario.strip()) < 3:
        return False

    if len(senha.strip()) < 3:
        return False

    # -------- Regras futuras --------
    # Aqui no futuro você pode:
    # - validar hash
    # - consultar banco
    # - gerar token
    # - usar OAuth / JWT

    return True
