# Interface Web — Agente Industrial Inteligente

Esta pasta contém a **interface web** do Desafio_FIESC, desenvolvida em [Streamlit](https://streamlit.io/), que permite ao usuário interagir com o agente conversacional por meio de um chat simples, sem precisar usar Jupyter Notebook ou conhecer SQL.

---

## 🚀 Como Executar

### 1. Abra o terminal e acesse este diretório:
   ```bash
   cd entregas_adicionais/interface_web
  ```

### 2. Ative o ambiente Python já configurado (recomenda-se o mesmo usado no notebook):

conda activate desafio_FIESC

### 3. ou, se usar virtualenv:

source venv/bin/activate   # Windows: venv\Scripts\activate

### 4. Instale as dependências necessárias:

pip install -r requirements.txt

### 5. Certifique-se de que o arquivo manutencao_industrial.db está nesta mesma pasta.

### 6. Execute o app:

streamlit run app.py

### 7. O aplicativo estará disponível em http://localhost:8501.


# O que muda nesta versão?
## Perguntas como “Qual a especialidade dele?” são respondidas com base no técnico mencionado na pergunta anterior, mesmo que não haja menção direta ao nome.

# Contexto é preservado durante toda a sessão no navegador.

# Perguntas de Teste Sugeridas

Quem trabalhou na ordem 3?

Qual a especialidade dele?

Quem trabalhou na ordem 4?

Qual a especialidade dele?
