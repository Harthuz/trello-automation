import os
import json
from mcp.server.fastmcp import FastMCP
from trello_integrator import TrelloClient

# Inicializa o servidor MCP do Trello
mcp = FastMCP("Trello Automation")

@mcp.tool()
def create_sprint_on_trello(sprint_json_string: str) -> str:
    """
    Cria um quadro, listas, etiquetas, cartões e checklists no Trello a partir de um JSON formatado na DSL de Sprints.
    
    Args:
        sprint_json_string (str): A string JSON contendo a estrutura de quadro, listas, labels e cards a serem criados.
    """
    # Resgata chaves do ambiente configuradas no Claude Desktop
    api_key = os.environ.get("TRELLO_API_KEY")
    token = os.environ.get("TRELLO_TOKEN")
    
    if not api_key or not token:
        return "Erro: As variáveis de ambiente TRELLO_API_KEY e TRELLO_TOKEN precisam estar configuradas no cliente MCP."
        
    try:
        dsl_data = json.loads(sprint_json_string)
    except Exception as e:
        return f"Erro de sintaxe no JSON: {str(e)}. Certifique-se de enviar um JSON válido."
        
    client = TrelloClient(api_key, token)
    
    try:
        # 1. Obter ou Criar o Quadro
        board_cfg = dsl_data.get("board", {})
        board_name = board_cfg.get("name", "Nova Sprint Trello")
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
        created_cards_summary = []
        for card_cfg in dsl_data.get("cards", []):
            card_title = card_cfg["title"]
            target_list_name = card_cfg["list"]
            card_desc = card_cfg.get("description", "")
            card_labels = card_cfg.get("labels", [])
            checklist_items = card_cfg.get("checklist", [])

            # Resgata o ID da lista correspondente
            list_id = lists_map.get(target_list_name)
            if not list_id:
                continue

            # Traduz nomes de etiquetas para IDs
            label_ids = [labels_map[name] for name in card_labels if name in labels_map]

            # Cria o cartão no Trello
            card = client.create_card(list_id, card_title, card_desc, label_ids)
            card_id = card["id"]

            # Adiciona checklist se houver itens
            if checklist_items:
                checklist = client.create_checklist(card_id)
                checklist_id = checklist["id"]
                for item in checklist_items:
                    client.add_checklist_item(checklist_id, item)
            
            created_cards_summary.append(f"- {card_title} (na lista '{target_list_name}')")
            
        cards_list_str = "\n".join(created_cards_summary)
        return (f"Sucesso! Quadro '{board_name}' criado/atualizado com sucesso no Trello.\n"
                f"Listas ativas: {list(lists_map.keys())}\n"
                f"Cartões criados:\n{cards_list_str}")
                
    except Exception as e:
        return f"Erro inesperado durante a integração: {str(e)}"

if __name__ == "__main__":
    # Inicia o servidor MCP local em modo STDIO (padrão do protocolo)
    mcp.run()
