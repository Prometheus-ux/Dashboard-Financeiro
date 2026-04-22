# Dashboard Financeiro

Dashboard pessoal para controle financeiro com Streamlit.

## Funcionalidades

- **Login** - Autenticação simples
- **Registrar transações** - Entradas e saídas
- **Métricas** - Visualizar totais de entradas, saídas e saldo
- **Gráfico de gastos** - Barras por categoria
- **Histórico mensal** - Filtro por mês/ano

## Tecnologias

- Python 3.10+
- Streamlit
- Pandas (para gráficos)
- CSV (persistência)

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

```bash
python -m streamlit run app.py
```

Acesse em: http://localhost:8501

## Categorias Disponíveis

- Salário
- Lazer
- Alimentação
- Educação
- Compras

## Estrutura de Dados

Registros salvos em `database/registros.csv`:

| Campo | Descrição |
|-------|-----------|
| usuario_id | Identificador do usuário |
| data | Data (YYYY-MM-DD) |
| descricao | Descrição do registro |
| valor | Valor em R$ |
| categoria | Categoria da transação |
| tipo | Entrada ou Saída |

## Login Padrão

O sistema aceita qualquer usuário com +3 caracteres. Configure `auth.py` para produção.