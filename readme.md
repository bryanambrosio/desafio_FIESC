# Desafio_FIESC — Agente Industrial Inteligente

**Autor:** Bryan Ambrósio  
**Data:** Junho/2025

---

## Apresentação

Este repositório reúne as soluções propostas para o **Desafio_FIESC — Agente Industrial Inteligente**.  
O desafio consiste em criar um agente conversacional capaz de interpretar perguntas em linguagem natural e traduzi-las em consultas SQL sobre um banco de dados industrial, democratizando o acesso à informação para operadores, engenheiros e gestores.

A estrutura do projeto está organizada em pastas temáticas, separando a entrega obrigatória das entregas diferenciais/adicionais, de forma modular e independente para facilitar a avaliação.

---

## 📂 Estrutura de Pastas

- **1_entrega_obrigatoria/**  
  Contém a entrega principal obrigatória, incluindo:
  - Jupyter Notebook (`desafio_FIESC.ipynb`) com código comentado, exemplos e explicações.
  - Banco de dados SQLite (`manutencao_industrial.db`) utilizado como base.
  - Diagrama da arquitetura da solução (`Diagrama.png`).
  - `readme.md` com instruções detalhadas de uso e exemplos de perguntas suportadas.

- **2_entregas_adicionais/**  
  Contém as implementações diferenciais (não obrigatórias), organizadas em subpastas independentes:
  
    - **cons_mult_tab/**  
      Consulta de múltiplas tabelas, suportando joins, agregações e filtros temporais.
      - `app.py` (Streamlit)
      - `requirements.txt`
      - `readme.md`

    - **interf_web/**  
      Interface web básica do agente via Streamlit.
      - `app.py`
      - `requirements.txt`
      - `manutencao_industrial.db`
      - `readme.md`

    - **mem_context/**  
      Versão com **memória de contexto** para perguntas encadeadas.
      - `app.py`
      - `requirements.txt`
      - `readme.md`

---

## Orientações Gerais

- Consulte sempre o `readme.md` de cada subpasta para detalhes de execução, exemplos de perguntas e diferenciais implementados.
- Use o ambiente `conda` ou `venv` recomendado para instalar as dependências de cada entrega.
- As entregas diferenciais são independentes entre si: pode testar cada uma separadamente, conforme sua preferência.

---

## Contato

Em caso de dúvidas ou sugestões, contate:
**Bryan Ambrósio**  
basa0492@hotmail.com

---

Desenvolvido para o processo seletivo FIESC/SENAI — Junho de 2025.
