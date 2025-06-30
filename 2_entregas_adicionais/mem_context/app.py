import streamlit as st
import sqlite3
import pandas as pd
import re
from datetime import datetime, timedelta
from typing import Tuple  # <-- Importa Tuple para type hint

# --- 1) Conexão com o Banco SQLite ---
db_path = 'manutencao_industrial.db'
conn = sqlite3.connect(db_path, check_same_thread=False)

# --- 2) Inicialização do contexto e histórico ---
if 'context' not in st.session_state:
    st.session_state.context = {}
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 3) Função de Parsing: NL → SQL com contexto ---
def nl_to_sql(query: str, context: dict) -> Tuple[str, dict]:
    """
    Parser NL→SQL com suporte a memória de contexto para perguntas encadeadas.
    """
    q = query.lower()
    ctx = context.copy()  # copia o contexto para atualizar se necessário

    # 1) Pergunta: Quem trabalhou na ordem X?
    m_ordem = re.search(r'ordem (\d+)', q)
    if 'quem' in q and m_ordem:
        ordem_id = int(m_ordem.group(1))
        ctx['ultimo_id_ordem'] = ordem_id
        return (
            "SELECT t.nome FROM tecnicos t "
            "JOIN ordem_tecnico ot ON t.id_tecnico = ot.id_tecnico "
            f"WHERE ot.id_ordem = {ordem_id}",
            ctx
        )

    # 2) Pergunta: Qual a especialidade dele/dela? (usa memória)
    if 'especialidade' in q and ('dele' in q or 'dela' in q or 'do técnico' in q):
        if ctx.get('ultimo_id_ordem') is not None:
            ordem_id = ctx['ultimo_id_ordem']
            return (
                "SELECT t.especialidade FROM tecnicos t "
                "JOIN ordem_tecnico ot ON t.id_tecnico = ot.id_tecnico "
                f"WHERE ot.id_ordem = {ordem_id}",
                ctx
            )
        else:
            return ("", ctx)

    # 3) Equipamentos em manutenção
    if 'equipamentos' in q and 'manutenção' in q:
        return ("SELECT * FROM equipamentos WHERE status LIKE '%manutenção%'", ctx)

    # 4) Ordens abertas em um setor específico
    m_setor = re.search(r'setor (\w+)', q)
    if 'ordens abertas' in q and m_setor:
        setor = m_setor.group(1).capitalize()
        return (
            "SELECT o.* "
            "FROM ordens_manutencao o "
            "JOIN equipamentos e ON o.id_equipamento = e.id_equipamento "
            f"WHERE o.status = 'aberta' AND e.localizacao = '{setor}'",
            ctx
        )

    # 5) Técnicos de elétrica no turno noturno
    if 'técnicos' in q and 'elétrica' in q and 'noturno' in q:
        return ("SELECT * FROM tecnicos WHERE especialidade = 'elétrica' AND turno = 'noturno'", ctx)

    # 6) Tempo médio de manutenção corretiva das bombas
    if 'tempo médio' in q and 'corretiva' in q and 'bombas' in q:
        return (
            "SELECT AVG(julianday(data_conclusao) - julianday(data_abertura)) AS media_dias "
            "FROM ordens_manutencao o "
            "JOIN equipamentos e ON o.id_equipamento = e.id_equipamento "
            "WHERE tipo_manutencao = 'corretiva' AND e.tipo = 'Bomba'",
            ctx
        )

    # 7) Ordens concluídas
    if 'ordens' in q and 'concluída' in q:
        return ("SELECT * FROM ordens_manutencao WHERE status = 'concluída'", ctx)

    # 8) Ordens de manutenção nos últimos N dias
    m_dias = re.search(r'últimos (\d+) dias', q)
    if 'ordens' in q and m_dias:
        dias = int(m_dias.group(1))
        data_limite = (datetime.now() - timedelta(days=dias)).strftime('%Y-%m-%d')
        return (f"SELECT * FROM ordens_manutencao WHERE date(data_abertura) >= '{data_limite}'", ctx)

    # 9) Contagem de técnicos por especialidade
    if 'quantos técnicos' in q and 'especialidade' in q:
        return (
            "SELECT especialidade, COUNT(*) AS total_tecnicos "
            "FROM tecnicos "
            "GROUP BY especialidade",
            ctx
        )

    # 10) Histórico de técnicos de uma ordem específica (redundante com 1, mas mantém)
    if 'quem' in q and m_ordem:
        ordem_id = m_ordem.group(1)
        return (
            "SELECT t.* "
            "FROM tecnicos t "
            "JOIN ordem_tecnico ot ON t.id_tecnico = ot.id_tecnico "
            f"WHERE ot.id_ordem = {ordem_id}",
            ctx
        )

    return ("", ctx)

# --- 4) Layout da página ---
st.title(" Agente Industrial Inteligente (Memória de Contexto)")

pergunta = st.text_input("Faça sua pergunta:")

if st.button("Enviar") and pergunta:
    sql, novo_ctx = nl_to_sql(pergunta, st.session_state.context)
    st.session_state.context = novo_ctx  # Atualiza contexto após cada pergunta
    if not sql:
        resposta = "❌ Desculpe, não entendi a pergunta."
    else:
        df = pd.read_sql(sql, conn)
        if 'media_dias' in df.columns:
            media = df['media_dias'].iloc[0]
            resposta = f"🕒 Tempo médio de manutenção corretiva das bombas: {media:.2f} dias"
        elif df.empty:
            resposta = "_(sem resultados)_"
        else:
            resposta = df.to_markdown(index=False)
    st.session_state.history.append((pergunta, resposta))

for q, r in st.session_state.history:
    st.markdown(f"**Você:** {q}")
    st.markdown(f"**Agente:**\n{r}")
