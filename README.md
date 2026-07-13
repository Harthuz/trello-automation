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

Você pode instalar a ferramenta localmente de forma global no seu computador executando o seguinte comando no diretório do projeto:

```powershell
pip install -e .
```
* *Explicação:* O parâmetro `-e` (editable) instala a ferramenta em modo de desenvolvimento. Isso cria o comando global `trello-integrator` no seu terminal, permitindo que você execute a automação de qualquer lugar apenas digitando:
  ```powershell
  trello-integrator caminho/para/sprint.json
  ```

---

## 🤖 Como Usar Como uma Skill de IA

1. **Alimente a IA:** Forneça as diretrizes contidas em `agent.md` para o seu chat de IA favorito.
2. **Peça o Planejamento:** Peça para a IA sugerir uma solução para o seu problema. Após a sua aprovação, peça para ela gerar o JSON da Sprint no formato especificado.
3. **Execute:** Salve o JSON gerado e use a CLI (`trello-integrator`) para subir o plano instantaneamente.