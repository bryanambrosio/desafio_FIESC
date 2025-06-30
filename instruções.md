# Desafio: Agente Industrial Inteligente

## Contexto

A Empresa X, uma empresa de médio porte do setor metalmecânico, iniciou recentemente a transformação digital de sua planta industrial. Como primeiro passo, a empresa passou a estruturar e armazenar dados de manutenção de seus equipamentos industriais, centralizando essas informações em um banco de dados relacional local.

Esse banco inclui informações como:

- Detalhes dos equipamentos instalados;
- Ordens de manutenção com histórico de intervenções;
- Técnicos envolvidos nas manutenções, suas especialidades e turnos.

Embora os dados estejam disponíveis, a equipe de engenharia ainda enfrenta dificuldades para extrair valor prático dessas informações. A maior parte das consultas depende de operadores que conheçam SQL e compreendam a estrutura do banco, o que limita a democratização do acesso à informação.

Para tornar o processo mais ágil e acessível, a diretoria técnica decidiu testar a implementação de um agente inteligente capaz de interpretar perguntas em linguagem natural e responder com base nas informações contidas no banco de dados.

A expectativa é que esse sistema possa ser utilizado por operadores de chão de fábrica, engenheiros de manutenção e gestores, cada um com diferentes necessidades e níveis de conhecimento técnico.

## Objetivo

Desenvolver uma aplicação baseada em inteligência artificial que permita que usuários façam perguntas em linguagem natural e recebam respostas contextualizadas e coerentes, baseadas no banco de dados relacional `manutencao_industrial.db`.

O sistema deve permitir que diferentes níveis de usuários, como operadores, engenheiros e gestores, façam perguntas utilizando linguagem natural para obter respostas úteis.

Além do funcionamento correto da aplicação, também será avaliada a clareza da arquitetura desenvolvida e sua capacidade de comunicar tecnicamente como os diferentes componentes da solução interagem entre si.

## Dados

Será disponibilizado um arquivo de banco de dados no formato SQLite (`.db`), contendo informações de planta industrial simulada. O arquivo está acessível para download por meio do link abaixo:

[Download: manutencao_industrial.db](https://drive.google.com/file/d/1B4l59bdPycqB4peRQxrrgOIlmGkGi-0v/view?usp=sharing)

Esse conjunto de dados deve ser utilizado como base para o desenvolvimento da aplicação. **Não é permitido modificar sua estrutura**, mas é possível realizar consultas, visualizações e inferências a partir dele.

---

## Entregas Obrigatórias

1. **Notebook com Código Funcional:**
   - Código organizado e comentado;
   - Interpretação de perguntas simples em linguagem natural;
   - Execução da consulta no banco de dados e retorno da resposta;
   - Exemplos de uso no próprio notebook.
2. **Desenho da Arquitetura:**
   - Imagem ou PDF com o fluxo da solução (componentes, dados, modelo, etc.).
3. **README.md:**
   - Explicação do projeto;
   - Como executar o código;
   - Exemplos de perguntas suportadas;
   - Limitações ou sugestões de melhoria.

> **OBSERVAÇÃO:** O código deve ser disponibilizado em um repositório **PÚBLICO** (no momento da submissão) no GitHub.

---

## Entregas Adicionais (Diferenciais, Não Obrigatórios)

1. **Interface Web tipo chat:**
   - Implementada em Streamlit, Gradio ou outra biblioteca;
   - Funcionalidades:
     - Campo de entrada para perguntas;
     - Exibição da resposta;
     - Histórico da conversa durante a sessão.

2. **Memória de Contexto:**
   - A comunicação deve manter o contexto para interpretações mais fluidas;
   - Agente capaz de interpretar perguntas em sequência contextual:
     - Exemplo:
       - Pergunta 1: “Qual técnico trabalhou na ordem 32?”
       - Pergunta 2 (sequência): “Qual a especialidade dele?”

3. **Consultas com múltiplas tabelas:**
   - Suporte a perguntas que envolvem junções de tabelas, como:
     - “Quais os tipos de equipamentos que tiveram manutenção nos últimos 3 meses?”
     - “Qual o nome do técnico que trabalhou em mais ordens de manutenção?”

> **OBSERVAÇÃO:** O código deve ser disponibilizado em um repositório **PÚBLICO** (no momento da submissão) no GitHub.
