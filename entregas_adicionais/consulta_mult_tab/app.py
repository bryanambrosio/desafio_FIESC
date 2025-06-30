import streamlit as st
import sqlite3
import pandas as pd
import re
from datetime import datetime, timedelta
from typing import Tuple

# --- 1) Conexão com o Banco SQLite ---
db_path = 'manutencao_industrial.db'
conn = sqlite3.connect(db_path, check_same_thread=False)

# --- 2) Inicialização do contexto e histórico ---
if 'context' not in st.session_state:
    st.session_state.context = {}
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 3) Função de Parsing: NL → SQL (joins + memória de contexto) ---
def nl_to_sql(query: str, context: dict) -> Tuple[str, dict]:
    q = query.lower()
    ctx = context.copy()

    # DIFERENCIAL 1: Tipos de equipamentos que tiveram manutenção nos últimos 3 meses
    if ('tipo' in q or 'tipos' in q) and 'equipamento' in q and 'manutenção' in q and ('mes' in q or 'mês' in q or 'meses' in q):
        data_limite = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
        return (
            "SELECT DISTINCT e.tipo "
            "FROM equipamentos e "
            "JOIN ordens_manutencao o ON o.id_equipamento = e.id_equipamento "
            f"WHERE o.data_abertura >= '{data_limite}'",
            ctx
        )

    # DIFERENCIAL 2: Técnico que trabalhou em mais ordens de manutenção
    if ('técnico' in q or 'tecnico' in q) and 'mais ordens' in q:
        return (
            "SELECT t.nome, COUNT(*) as total_ordens "
            "FROM tecnicos t "
            "JOIN ordem_tecnico ot ON t.id_tecnico = ot.id_tecnico "
            "GROUP BY t.nome "
            "ORDER BY total_ordens DESC "
            "LIMIT 1",
            ctx
        )

    # 1) Pergunta: Quem trabalhou na ordem X? (memória de contexto)
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

    # Regras clássicas (independentes)
    if 'equipamentos' in q and 'manutenção' in q:
        return ("SELECT * FROM equipamentos WHERE status LIKE '%manutenção%'", ctx)

    m_setor = re.search(r'setor (\\w+)', q)
    if 'ordens abertas' in q and m_setor:
        setor = m_setor.group(1).capitalize()
        return (
            "SELECT o.* "
            "FROM ordens_manutencao o "
            "JOIN equipamentos e ON o.id_equipamento = e.id_equipamento "
            f"WHERE o.status = 'aberta' AND e.localizacao = '{setor}'",
            ctx
        )

    if 'técnicos' in q and 'elétrica' in q and 'noturno' in q:
        return ("SELECT * FROM tecnicos WHERE especialidade = 'elétrica' AND turno = 'noturno'", ctx)

    if 'tempo médio' in q and 'corretiva' in q and 'bombas' in q:
        return (
            "SELECT AVG(julianday(data_conclusao) - julianday(data_abertura)) AS media_dias "
            "FROM ordens_manutencao o "
            "JOIN equipamentos e ON o.id_equipamento = e.id_equipamento "
            "WHERE tipo_manutencao = 'corretiva' AND e.tipo = 'Bomba'",
            ctx
        )

    if 'ordens' in q and 'concluída' in q:
        return ("SELECT * FROM ordens_manutencao WHERE status = 'concluída'", ctx)

    m_dias = re.search(r'últimos (\\d+) dias', q)
    if 'ordens' in q and m_dias:
        dias = int(m_dias.group(1))
        data_limite = (datetime.now() - timedelta(days=dias)).strftime('%Y-%m-%d')
        return (f"SELECT * FROM ordens_manutencao WHERE date(data_abertura) >= '{data_limite}'", ctx)

    if 'quantos técnicos' in q and 'especialidade' in q:
        return (
            "SELECT especialidade, COUNT(*) AS total_tecnicos "
            "FROM tecnicos "
            "GROUP BY especialidade",
            ctx
        )

    return ("", ctx)

# --- 4) Layout da página ---
st.title("🤖 Agente Industrial Inteligente — Multitabela + Memória de Contexto")

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
