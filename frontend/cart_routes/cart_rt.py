from flask import Blueprint, render_template, request, session

import requests

router = Blueprint("cart_rt", __name__)
API_URL_CART = "http://127.0.0.1:8003"

@router.app_template_filter('floatformat')
def floatformat(value, decimal_places=2):
    try:
        return f"{value:.{decimal_places}f}"
    except (ValueError, TypeError):
        return value
    
def capitalize_first_letter(text):
    return text.capitalize()
    
# Rota do carrinho de compras
@router.route("/carrinho")
def index():
    """
    Exibe os itens do carrinho do usuário com base no user_id da query string.
    Consulta o microsserviço de vendas.
    """
    try:
        user_id = int(request.args.get("user_id", 0)) 
    except Exception as e:
        return render_template("cart.html", error_message="Usuário precisa está logado")

    try:
        response = requests.get(f'{API_URL_CART}/cart/{user_id}')

        if response.status_code == 400:
            detail = response.json().get("detail", "Sem produtos")
            return render_template("cart.html", error_message=detail)
        
        data = response.json()
        

        return render_template(
            "cart.html",
            order_id=data["id"],
            items=data["items"],
            total=data["total"],
            features=session.get("features", [])  # <- aqui
        )
    
    except Exception as e:
        return f"Erro ao acessar no arquivo cart_rt: {e}"

# Rota que renderiza os pedidos (simplesmente carrega a página)
@router.route("/orders")
def orders():
    return render_template("order.html")