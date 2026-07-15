# Trello Automation CLI & AI Skill

Este repositório contém uma ferramenta CLI em Python projetada para automatizar a criação e gerenciamento de quadros (Boards), listas (Lists), etiquetas (Labels), cartões (Cards) e checklists no Trello a partir de um arquivo JSON estruturado (DSL), eliminando fluxos manuais de CSV.

Além de rodar localmente no seu terminal, esta ferramenta foi estruturada para ser importada como uma **Skill de IA**, permitindo que agentes de IA (como Claude, Antigravity, etc.) preparem e executem o seu planejamento ágil diretamente no Trello.

---

## 📂 Estrutura do Projeto

* **`trello_integrator.py`**: O script principal que faz a comunicação direta e inteligente com a API do Trello.
* **`pyproject.toml`**: Configuração de empacotamento padrão Python para tornar a CLI instalável via `pip`.
* **`skill_manifest.json`**: Manifesto de integração da ferramenta para ser consumida como *skill* por outros agentes de IA.
* **`manual/`**:
  * [architecture.md](manual/architecture.md): Fluxo de dados e arquitetura de integração.
  * [dsl_spec.md](manual/dsl_spec.md): Especificação detalhada da estrutura do JSON de entrada.
  * [setup_guide.md](manual/setup_guide.md): Guia passo a passo para gerar as credenciais do Trello.
* **`agent.md`**: Perfil de comportamento instrucional para alimentar a IA parceira e ensiná-la a planejar em Sprints JSON.

---

## 🚀 Como Instalar Localmente (Modo CLI)

Você tem duas formas principais de instalar o utilitário em seu computador usando o terminal/Command Prompt (CMD):

### Opção A: Instalar via PyPI (Recomendado para uso geral)
Abra o Prompt de Comando (CMD) e execute o comando abaixo para baixar e instalar o pacote oficial publicado:
```cmd
pip install trello-automation-cli
```
*(Caso o comando `pip` não seja reconhecido no seu CMD, utilize: `python -m pip install trello-automation-cli`)*

### Opção B: Instalar a partir do repositório clonado (Desenvolvimento)
Navegue até a pasta do repositório clonado pelo Prompt de Comando (CMD) e execute:
```cmd
pip install -e .
```

---

## 💻 Como Utilizar pelo Prompt de Comando (CMD)

Após a instalação, você pode executar o integrador de duas formas no Windows:

### 1. Usando o comando global (Se as variáveis de ambiente PATH estiverem configuradas no Windows)
No seu CMD, execute passando o arquivo JSON de definição de Sprint:
```cmd
trello-integrator caminho/para/sprint_definition.json
```

### 2. Chamando o script Python diretamente (Método mais compatível e seguro)
Se o comando global não for encontrado, execute usando o Python diretamente do diretório raiz do projeto:
```cmd
python trello-automation/trello_integrator.py caminho/para/sprint_definition.json
```

---

## 🤖 Como Usar Como uma Skill de IA

1. **Alimente a IA:** Forneça as diretrizes contidas em `agent.md` para o seu chat de IA favorito.
2. **Peça o Planejamento:** Peça para a IA sugerir uma solução para o seu problema. Após a sua aprovação, peça para ela gerar o JSON da Sprint no formato especificado.
3. **Execute:** Salve o JSON gerado e use a CLI (`trello-integrator`) para subir o plano instantaneamente.