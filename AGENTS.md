# AGENTS.md

## Visão Geral

Dashboard Financeiro pessoal criado com Streamlit para controle de entradas e saídas.

## Estrutura do Projeto

```
├── app.py                    # Interface principal (Streamlit)
├── auth.py                 # Autenticação simples
├── services/
│   └── finance.py         # Lógica de cálculos financeiros
├── database/
│   └── storage.py         # Persistência em CSV
├── utils/
│   └── validators.py      # Validação de dados
└── requirements.txt       # Dependências Python
```

## Comandos de Execução

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar aplicação
python -m streamlit run app.py
```

## Funcionalidades

- Login com usuário/senha
- Registrar receitas e despesas
- Visualizar métricas (entradas, saídas, saldo)
- Gráfico de gastos por categoria
- Histórico mensal com filtros

## Convenções de Código

- Funções em snake_case
- Tipagem: Type hints em todas as funções públicas
- Comentários apenas quando necessário
- CSV com encoding UTF-8
- Formato de data: YYYY-MM-DD

## Autenticação (MVP)

O módulo `auth.py` implementa autenticação básica:
- Valida长度 mínima de usuário/senha (3 caracteres)
- Futura integração: hash, banco de dados, JWT

## Persistência

Dados salvos em `database/registros.csv`:
- `usuario_id`: identificador do usuário
- `data`: data no formato YYYY-MM-DD
- `descricao`: descrição do registro
- `valor`: valor numérico
- `categoria`: Salário|Lazer|Alimentação|Educação|Compras
- `tipo`: Entrada|Saída