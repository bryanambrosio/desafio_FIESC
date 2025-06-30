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


### Funcionalidades
Chat em linguagem natural: envie perguntas como faria a uma pessoa.

Tradução NL→SQL: o agente interpreta sua pergunta e gera a consulta SQL correspondente (visualizável em um expander).

Resposta contextualizada: resultados em tabela interativa ou mensagem indicando ausência de dados.

### Exemplos de Perguntas Suportadas

Quais equipamentos estão atualmente em manutenção?

Quem são os técnicos de elétrica no turno noturno?

Qual foi o tempo médio de manutenção corretiva das bombas?
