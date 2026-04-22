import streamlit as st
from datetime import datetime

from auth import autenticar
from services.finance import (
    calcular_entradas,
    calcular_saidas,
    calcular_saldo,
    gastos_por_categoria,
    filtrar_por_mes
)
from database.storage import carregar_dados, salvar_registro


# ======================
# CONFIGURAÇÃO
# ======================
st.set_page_config(
    page_title="Dashboard Financeiro",
    layout="wide"
)


# ======================
# ESTADOS GLOBAIS
# ======================
st.session_state.setdefault("logado", False)
st.session_state.setdefault("usuario", None)
st.session_state.setdefault("registro_salvo", False)


# ======================
# LOGIN
# ======================
def tela_login():
    st.title("🔐 Login")

    with st.form("form_login"):
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        entrar = st.form_submit_button("Entrar")

        if entrar:
            if autenticar(usuario, senha):
                st.session_state.logado = True
                st.session_state.usuario = usuario
                st.rerun()
            else:
                st.error("❌ Usuário ou senha inválidos")


# ======================
# FORMULÁRIO DE REGISTRO
# ======================
def formulario_registro():
    with st.expander("➕ Novo Registro"):
        with st.form("form_registro", clear_on_submit=True):
            data = st.date_input("Data", value=datetime.today())
            descricao = st.text_input("Descrição")
            valor = st.number_input("Valor", min_value=0.01, step=0.01)
            categoria = st.selectbox(
                "Categoria",
                ["Salário", "Lazer", "Alimentação", "Educação", "Compras"]
            )
            tipo = st.selectbox("Tipo", ["Entrada", "Saída"])

            salvar = st.form_submit_button("Salvar")

            if salvar:
                registro = {
                    "usuario_id": st.session_state.usuario,
                    "data": data,
                    "descricao": descricao,
                    "valor": float(valor),
                    "categoria": categoria,
                    "tipo": tipo
                }

                salvar_registro(registro)
                st.session_state.registro_salvo = True
                st.rerun()


# ======================
# HISTÓRICO MENSAL
# ======================
def historico_mensal(registros):
    st.subheader("📊 Histórico Mensal")

    col1, col2 = st.columns(2)

    with col1:
        mes = st.selectbox(
            "Mês",
            range(1, 13),
            index=datetime.now().month - 1
        )

    with col2:
        ano = st.selectbox(
            "Ano",
            range(2024, 2031),
            index=2
        )

    registros_mes = filtrar_por_mes(registros, ano, mes)

    if not registros_mes:
        st.info("Nenhum registro neste mês.")
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("Entradas", f"R$ {calcular_entradas(registros_mes):,.2f}")
    c2.metric("Saídas", f"R$ {calcular_saidas(registros_mes):,.2f}")
    c3.metric("Saldo", f"R$ {calcular_saldo(registros_mes):,.2f}")


# ======================
# DASHBOARD
# ======================
def dashboard():
    st.title("📊 Dashboard Financeiro")

    registros = carregar_dados(st.session_state.usuario)

    if st.session_state.registro_salvo:
        st.success("✅ Registro salvo com sucesso!")
        st.session_state.registro_salvo = False

    if registros:
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 Entradas", f"R$ {calcular_entradas(registros):,.2f}")
        col2.metric("💸 Saídas", f"R$ {calcular_saidas(registros):,.2f}")
        col3.metric("📈 Saldo", f"R$ {calcular_saldo(registros):,.2f}")

        st.subheader("📌 Gastos por Categoria")
        st.bar_chart(gastos_por_categoria(registros))
    else:
        st.info("📭 Nenhum registro encontrado.")

    formulario_registro()
    historico_mensal(registros)


# ======================
# CONTROLE PRINCIPAL
# ======================
if not st.session_state.logado:
    tela_login()
else:
    dashboard()
