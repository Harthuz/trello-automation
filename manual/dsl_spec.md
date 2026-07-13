# Especificação do Formato JSON (DSL)

O serviço local em Python consome um arquivo estruturado que define a configuração do Quadro e das tarefas. Abaixo está a especificação detalhada de cada campo suportado.

## Esquema Exemplo (`sprint_definition.json`)

```json
{
  "board": {
    "name": "Projeto GYM - Semana 1",
    "desc": "Quadro de automação de desenvolvimento do projeto GYM."
  },
  "lists": [
    "A Fazer (Sprint 1)",
    "Em Progresso",
    "Em Revisão",
    "Concluído"
  ],
  "labels": [
    {
      "name": "Funcionalidade",
      "color": "green"
    },
    {
      "name": "Refatoração",
      "color": "yellow"
    },
    {
      "name": "Erro/Bug",
      "color": "red"
    }
  ],
  "cards": [
    {
      "title": "Task 1.3: Implementar Excluir Exercício",
      "list": "A Fazer (Sprint 1)",
      "labels": ["Funcionalidade"],
      "description": "Adicionar opção no menu para excluir um exercício cadastrado filtrando pelo ID único ou nome.\n\n### Critérios de Aceitação:\n- Menu interativo solicita confirmação antes de excluir.\n- Remove o registro do arquivo json de dados.\n- Grava o log da exclusão.",
      "checklist": [
        "Criar fluxo de input no menu.py",
        "Implementar a função de remoção no storage/data",
        "Gravar log da exclusão no app.log",
        "Escrever teste unitário correspondente"
      ]
    },
    {
      "title": "Task 1.4: Implementar Editar Exercício",
      "list": "A Fazer (Sprint 1)",
      "labels": ["Funcionalidade", "Refatoração"],
      "description": "Adicionar opção no menu para editar os campos (nome, categoria, descrição) de um exercício cadastrado.",
      "checklist": [
        "Criar fluxo de edição no menu.py",
        "Atualizar o registro no json local",
        "Adicionar teste unitário no pytest"
      ]
    }
  ]
}
```

## Detalhes das Chaves

### 1. `board` (Objeto)
* `name` (Obrigatório): O nome do quadro do Trello que será criado ou utilizado.
* `desc` (Opcional): Uma breve descrição sobre o quadro.

### 2. `lists` (Array de Strings)
* Contém os nomes das listas ordenadas na tela. O serviço deve criá-las da esquerda para a direita, respeitando esta ordem.

### 3. `labels` (Array de Objetos)
* `name`: Nome identificador da etiqueta.
* `color`: Cor da etiqueta no Trello (ex: `green`, `yellow`, `orange`, `red`, `purple`, `blue`, `sky`, `lime`, `pink`, `black`).

### 4. `cards` (Array de Objetos)
* `title` (Obrigatório): Nome/Título do cartão.
* `list` (Obrigatório): Em qual lista este cartão deve ser inserido (deve corresponder a uma das strings definidas em `lists`).
* `labels` (Opcional): Array com os nomes das etiquetas associadas (devem corresponder a nomes definidos em `labels`).
* `description` (Opcional): Descrição em formato Markdown para o corpo do cartão.
* `checklist` (Opcional): Array de strings contendo tarefas a serem convertidas em uma checklist padrão dentro do cartão.
