# Interface Web — Agente Industrial Inteligente

Esta pasta contém a **interface web** do Desafio_FIESC, desenvolvida em [Streamlit](https://streamlit.io/), que permite ao usuário interagir com o agente conversacional por meio de um chat simples.

---

## 🚀 Como Executar

### 1. Abra o terminal e acesse este diretório:
   ```bash
   cd entregas_adicionais/interface_web
  ```

### 2. Ative o ambiente Python já configurado (recomenda-se o mesmo usado no notebook):
   ```bash
conda activate desafio_FIESC
  ```
### 3. ou, se usar virtualenv:
   ```bash
source venv/bin/activate   # Windows: venv\Scripts\activate
  ```
### 4. Instale as dependências necessárias:
   ```bash
pip install -r requirements.txt
  ```
### 5. Certifique-se de que o arquivo manutencao_industrial.db está nesta mesma pasta.

### 6. Execute o app:
   ```bash
streamlit run app.py
  ```
### 7. O aplicativo estará disponível em http://localhost:8501.


# O que muda nesta versão?

## Suporte a perguntas com múltiplas tabelas e operações agregadas (JOIN, GROUP BY, etc)

## Memória de contexto para perguntas encadeadas sobre ordens e técnicos

# Contexto é preservado durante toda a sessão no navegador.

# Perguntas de Teste Sugeridas

Quais os tipos de equipamentos que tiveram manutenção nos últimos 3 meses?

Qual o nome do técnico que trabalhou em mais ordens de manutenção?
