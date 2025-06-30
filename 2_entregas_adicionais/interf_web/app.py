import streamlit as st
import sqlite3
import pandas as pd
import re
from datetime import datetime, timedelta

# --- 1) Conexão com o Banco SQLite ---
# O arquivo 'manutencao_industrial.db' deve estar na mesma pasta deste script
db_path = 'manutencao_industrial.db'
conn = sqlite3.connect(db_path, check_same_thread=False)

# --- 2) Função de Parsing: NL → SQL ---
def nl_to_sql(query: str) -> str:
    """
    Converte uma pergunta em linguagem natural para uma query SQL.
    Suporta vários padrões:
      1) Equipamentos em manutenção
      2) Ordens abertas em um setor X
      3) Técnicos de elétrica no turno noturno
      4) Tempo médio de manutenção corretiva das bombas
      5) Ordens concluídas
      6) Ordens nos últimos N dias
      7) Contagem de técnicos por especialidade
      8) Histórico de técnicos de uma ordem específica
    """
    q = query.lower()

    # 1) Equipamentos em manutenção
    if 'equipamentos' in q and 'manutenção' in q:
        return "SELECT * FROM equipamentos WHERE status LIKE '%manutenção%'"

    # 2) Ordens abertas em um setor específico
    if 'ordens abertas' in q:
        m = re.search(r'setor (\w+)', q)
        if m:
            setor = m.group(1).capitalize()
            return (
                "SELECT o.* "
                "FROM ordens_manutencao o "
                "JOIN equipamentos e ON o.id_equipamento = e.id_equipamento "
                f"WHERE o.status = 'aberta' AND e.localizacao = '{setor}'"
            )

    # 3) Técnicos de elétrica no turno noturno
    if 'técnicos' in q and 'elétrica' in q and 'noturno' in q:
        return "SELECT * FROM tecnicos WHERE especialidade = 'elétrica' AND turno = 'noturno'"

    # 4) Tempo médio de manutenção corretiva das bombas
    if 'tempo médio' in q and 'corretiva' in q and 'bombas' in q:
        return (
            "SELECT AVG(julianday(data_conclusao) - julianday(data_abertura)) AS media_dias "
            "FROM ordens_manutencao o "
            "JOIN equipamentos e ON o.id_equipamento = e.id_equipamento "
            "WHERE tipo_manutencao = 'corretiva' AND e.tipo = 'Bomba'"
        )

    # 5) Ordens concluídas
    if 'ordens' in q and 'concluída' in q:
        return "SELECT * FROM ordens_manutencao WHERE status = 'concluída'"

    # 6) Ordens de manutenção nos últimos N dias
    m = re.search(r'últimos (\d+) dias', q)
    if 'ordens' in q and m:
        dias = int(m.group(1))
        data_limite = (datetime.now() - timedelta(days=dias)).strftime('%Y-%m-%d')
        return f"SELECT * FROM ordens_manutencao WHERE date(data_abertura) >= '{data_limite}'"

    # 7) Contagem de técnicos por especialidade
    if 'quantos técnicos' in q and 'especialidade' in q:
        return (
            "SELECT especialidade, COUNT(*) AS total_tecnicos "
            "FROM tecnicos "
            "GROUP BY especialidade"
        )

    # 8) Histórico de técnicos de uma ordem específica
    m = re.search(r'ordem (\d+)', q)
    if 'quem' in q and m:
        ordem_id = m.group(1)
        return (
            "SELECT t.* "
            "FROM tecnicos t "
            "JOIN ordem_tecnico ot ON t.id_tecnico = ot.id_tecnico "
            f"WHERE ot.id_ordem = {ordem_id}"
        )

    # Se nenhuma regra casar, retorna string vazia
    return ""

# --- 3) Histórico de sessão ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 4) Layout da página ---
st.title(" Agente Industrial Inteligente")

pergunta = st.text_input("Faça sua pergunta:")
if st.button("Enviar") and pergunta:
    # 4.1) Gera a SQL
    sql = nl_to_sql(pergunta)
    if not sql:
        resposta = "❌ Desculpe, não entendi a pergunta."
    else:
        # 4.2) Executa a query no banco
        df = pd.read_sql(sql, conn)
        # 4.3) Gera resposta específica para média
        if 'media_dias' in df.columns:
            media = df['media_dias'].iloc[0]
            resposta = f" Tempo médio de manutenção corretiva das bombas: {media:.2f} dias"
        else:
            # Converte DataFrame para visualização
            resposta = f"**SQL:** `{sql}`"
            if df.empty:
                resposta += "\n\n_(sem resultados)_"
            else:
                resposta += "\n\n" + df.to_markdown(index=False)
    # 4.4) Armazena no histórico
    st.session_state.history.append((pergunta, resposta))

# 4.5) Exibe todo o histórico de conversa
for q, r in st.session_state.history:
    st.markdown(f"**Você:** {q}")
    st.markdown(f"**Agente:**\n{r}")
