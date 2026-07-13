import os
import json
import sys
import requests

def load_env(env_path: str) -> dict:
    """Carrega variáveis de ambiente de um arquivo .env manualmente para evitar dependências externas."""
    config = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    config[key.strip()] = val.strip().strip('"').strip("'")
    return config

class TrelloClient:
    def __init__(self, api_key: str, token: str):
        self.api_key = api_key
        self.token = token
        self.base_url = "https://api.trello.com/1"
        self.auth_params = {
            "key": self.api_key,
            "token": self.token
        }

    def _request(self, method: str, path: str, params: dict = None, json_data: dict = None) -> dict:
        url = f"{self.base_url}{path}"
        request_params = self.auth_params.copy()
        if params:
            request_params.update(params)
        
        response = requests.request(method, url, params=request_params, json=json_data)
        if response.status_code not in (200, 201):
            raise Exception(f"Erro na requisição Trello [{response.status_code}]: {response.text}")
        return response.json()

    def get_my_boards(self) -> list:
        return self._request("GET", "/members/me/boards")

    def create_board(self, name: str, desc: str = "") -> dict:
        # Verifica se já existe um quadro com o mesmo nome para evitar duplicatas
        boards = self.get_my_boards()
        for b in boards:
            if b["name"] == name:
                print(f"Quadro '{name}' já existe (ID: {b['id']}). Reutilizando...")
                return b
        
        print(f"Criando novo quadro: '{name}'...")
        params = {"name": name, "defaultLists": "false"}
        if desc:
            params["desc"] = desc
        return self._request("POST", "/boards", params=params)

    def get_lists(self, board_id: str) -> list:
        return self._request("GET", f"/boards/{board_id}/lists")

    def create_list(self, board_id: str, name: str) -> dict:
        lists = self.get_lists(board_id)
        for l in lists:
            if l["name"] == name:
                print(f"  Lista '{name}' já existe. Reutilizando...")
                return l
        
        print(f"  Criando lista: '{name}'...")
        params = {"name": name, "idBoard": board_id, "pos": "bottom"}
        return self._request("POST", "/lists", params=params)

    def get_labels(self, board_id: str) -> list:
        return self._request("GET", f"/boards/{board_id}/labels")

    def create_label(self, board_id: str, name: str, color: str) -> dict:
        labels = self.get_labels(board_id)
        for label in labels:
            if label["name"] == name:
                # Se já existe etiqueta com esse nome, apenas retorna
                return label
        
        print(f"  Criando etiqueta: '{name}' ({color})...")
        params = {"name": name, "color": color, "idBoard": board_id}
        return self._request("POST", "/labels", params=params)

    def create_card(self, list_id: str, name: str, desc: str = "", label_ids: list = None) -> dict:
        params = {
            "name": name,
            "idList": list_id,
            "desc": desc
        }
        if label_ids:
            params["idLabels"] = ",".join(label_ids)
        
        return self._request("POST", "/cards", params=params)

    def create_checklist(self, card_id: str, name: str = "Tarefas") -> dict:
        params = {"idCard": card_id, "name": name}
        return self._request("POST", "/checklists", params=params)

    def add_checklist_item(self, checklist_id: str, name: str) -> dict:
        params = {"name": name}
        return self._request("POST", f"/checklists/{checklist_id}/checkItems", params=params)


def main():
    # Caminhos padrão
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    
    # Carrega variáveis
    env_vars = load_env(env_file)
    api_key = env_vars.get("TRELLO_API_KEY")
    token = env_vars.get("TRELLO_TOKEN")

    if not api_key or not token:
        print("Erro: TRELLO_API_KEY ou TRELLO_TOKEN não encontrados no arquivo .env")
        sys.exit(1)

    # Determina o arquivo DSL de entrada
    dsl_file = "sprint_definition.json"
    if len(sys.argv) > 1:
        dsl_file = sys.argv[1]

    if not os.path.exists(dsl_file):
        print(f"Erro: Arquivo DSL '{dsl_file}' não encontrado.")
        print("Crie um arquivo contendo a definição da sprint no mesmo diretório.")
        sys.exit(1)

    print(f"Lendo definição da sprint de '{dsl_file}'...")
    with open(dsl_file, "r", encoding="utf-8") as f:
        dsl_data = json.load(f)

    # Inicializa cliente
    client = TrelloClient(api_key, token)

    # 1. Obter ou Criar o Quadro
    board_cfg = dsl_data.get("board", {})
    board_name = board_cfg.get("name", "Novo Quadro de Sprint")
    board_desc = board_cfg.get("desc", "")
    
    board = client.create_board(board_name, board_desc)
    board_id = board["id"]

    # 2. Criar Listas
    lists_map = {}
    for list_name in dsl_data.get("lists", []):
        lst = client.create_list(board_id, list_name)
        lists_map[list_name] = lst["id"]

    # 3. Criar Etiquetas
    labels_map = {}
    for label_cfg in dsl_data.get("labels", []):
        lbl_name = label_cfg["name"]
        lbl_color = label_cfg["color"]
        lbl = client.create_label(board_id, lbl_name, lbl_color)
        labels_map[lbl_name] = lbl["id"]

    # 4. Criar Cartões e Checklists
    print("\nProcessando cartões...")
    for card_cfg in dsl_data.get("cards", []):
        card_title = card_cfg["title"]
        target_list_name = card_cfg["list"]
        card_desc = card_cfg.get("description", "")
        card_labels = card_cfg.get("labels", [])
        checklist_items = card_cfg.get("checklist", [])

        # Resgata o ID da lista
        list_id = lists_map.get(target_list_name)
        if not list_id:
            print(f"  Aviso: Lista '{target_list_name}' não mapeada. Pulando cartão '{card_title}'...")
            continue

        # Traduz nomes de etiquetas para IDs
        label_ids = [labels_map[name] for name in card_labels if name in labels_map]

        # Cria o cartão
        print(f"  -> Criando cartão: '{card_title}' na lista '{target_list_name}'...")
        card = client.create_card(list_id, card_title, card_desc, label_ids)
        card_id = card["id"]

        # Adiciona checklist se houver itens
        if checklist_items:
            print(f"     Adicionando checklist ao cartão '{card_title}'...")
            checklist = client.create_checklist(card_id)
            checklist_id = checklist["id"]
            for item in checklist_items:
                client.add_checklist_item(checklist_id, item)

    print("\nIntegração concluída com sucesso! Verifique seu quadro no Trello.")

if __name__ == "__main__":
    main()
