# Guia de Configuração e Uso da API do Trello

Para que o script em Python faça requisições automáticas em sua conta do Trello, você precisa obter uma Chave de API (API Key) e gerar um Token de Acesso de Usuário (User Token).

---

## 1. Como Obter suas Credenciais

1. **Obtenha a API Key:**
   * Acesse o portal de desenvolvedores da Atlassian: [Trello Developer Start Portal](https://developer.atlassian.com/cloud/trello/guides/rest-api/authorization/).
   * Crie uma conta de desenvolvedor se solicitado e acesse a página de chaves de API.
   * Copie o valor exibido no campo **Personal Key (Chave Pessoal)**.

2. **Gere o User Token:**
   * Na mesma tela da Chave de API, haverá um link para gerar manualmente um token.
   * Alternativamente, você pode acessar a URL abaixo substituindo `{SUA_API_KEY}` pela chave pessoal que você obteve no passo anterior:
     ```text
     https://trello.com/1/authorize?expiration=never&scope=read,write,account&response_type=token&key={SUA_API_KEY}
     ```
   * Dê permissão para que o seu app acesse sua conta do Trello.
   * Copie o token de acesso gerado na tela.

---

## 2. Configurando o Ambiente Local

1. Recomenda-se criar um arquivo chamado `.env` na raiz do seu projeto independente para guardar estas credenciais de forma segura (e adicioná-lo no `.gitignore`):

```bash
# Conteúdo do arquivo .env
TRELLO_API_KEY="seu_valor_de_api_key_aqui"
TRELLO_TOKEN="seu_valor_de_token_aqui"
```

2. Instale a biblioteca `requests` para simplificar as chamadas HTTP em Python. Você pode fazer isso executando:
   ```bash
   pip install requests python-dotenv
   ```
   * *Explicação:* O `requests` permite fazer requisições HTTP REST com facilidade para a API do Trello, e o `python-dotenv` carrega as variáveis de ambiente salvas no arquivo `.env`.

---

## 3. Endpoints da API Úteis para o Script

* **Criar Quadro:** `POST /1/boards/?name={nome}&key={key}&token={token}`
* **Consultar Quadros:** `GET /1/members/me/boards?key={key}&token={token}`
* **Criar Lista:** `POST /1/lists?name={nome}&idBoard={id_quadro}&key={key}&token={token}`
* **Consultar Listas do Quadro:** `GET /1/boards/{id_quadro}/lists?key={key}&token={token}`
* **Criar Etiqueta:** `POST /1/labels?name={nome}&color={cor}&idBoard={id_quadro}&key={key}&token={token}`
* **Criar Cartão:** `POST /1/cards?name={titulo}&desc={markdown}&idList={id_lista}&idLabels={id_etiquetas}&key={key}&token={token}`
* **Criar Checklist:** `POST /1/checklists?idCard={id_cartao}&name=Tarefas&key={key}&token={token}`
* **Adicionar Item na Checklist:** `POST /1/checklists/{id_checklist}/checkItems?name={item}&key={key}&token={token}`
