---
name: trello-automation
description: Automatically plans and creates boards, lists, labels, cards, and checklists on Trello using a structured JSON DSL.
license: MIT
metadata:
  author: Harthuz
---

# Trello Automation Skill

This Model Context Protocol (MCP) server allows AI models (like Claude or Cursor) to automatically plan and create boards, lists, labels, cards, and checklists on Trello using a structured JSON DSL.

## When to activate
- User wants to create a new board, sprint, or task list on Trello.
- User wants to automate the creation of cards, labels, or checklists based on code changes or planning.

## Configuration (Environment Variables)

Para usar esta skill, você deve configurar as seguintes credenciais na configuração do seu cliente MCP (ex: Claude Desktop):

* `TRELLO_API_KEY`: A sua chave pessoal da API do Trello.
* `TRELLO_TOKEN`: O token de autorização de usuário do Trello.

## Ferramentas Disponíveis (Tools)

### `create_sprint_on_trello`

Cria a estrutura completa de uma Sprint (Quadro, Listas, Etiquetas, Cartões e Checklists) a partir de um JSON string.

**Parâmetros de Entrada:**
* `sprint_json_string` (string, obrigatório): String formatada em JSON contendo a definição da sprint.

**Exemplo de JSON DSL:**
```json
{
  "board": {
    "name": "Nome do Quadro",
    "desc": "Descrição do Quadro"
  },
  "lists": ["A Fazer", "Em Progresso", "Concluído"],
  "labels": [
    { "name": "Feature", "color": "green" }
  ],
  "cards": [
    {
      "title": "Minha Tarefa",
      "list": "A Fazer",
      "labels": ["Feature"],
      "description": "Descrição detalhada",
      "checklist": ["Passo 1", "Passo 2"]
    }
  ]
}
```
