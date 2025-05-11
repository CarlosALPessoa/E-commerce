from flask import Blueprint, render_template, request, session, redirect
import requests

router = Blueprint("router", __name__)

# Endereços dos microsserviços de catálogo e vendas
API_URL_BOOKS = "http://127.0.0.1:8002"
API_URL_SALES = "http://127.0.0.1:8003"

def capitalize_first_letter(text):
    return text.capitalize()

@router.app_template_filter('floatformat')
def floatformat(value, decimal_places=2):
    try:
        return f"{value:.{decimal_places}f}"
    except (ValueError, TypeError):
        return value

# Página principal (catálogo de livros)
@router.route('/')
def index():
    """
    Rota principal que lista os livros do catálogo.
    Consulta o microsserviço de catálogo e renderiza os livros formatados.
    """
    try:
        response = requests.get(f'{API_URL_BOOKS}/livros') #microsserviço de produtos
        livros = response.json()
        for livro in livros:
            livro['titulo'] = capitalize_first_letter(livro['titulo'])
        return render_template("catalog.html", livros=livros)
    except Exception as e:
        return f"Erro ao acessar a API: {e}"

# Página de registro de novo usuário
@router.route("/registrar")
def pagina_registro():
    return render_template("registro.html")

# Página com detalhes de um livro
@router.route('/livros/<int:id>') 
def livro(id):
    """
    Rota que exibe detalhes de um livro específico com base no ID.
    Consulta o microsserviço de catálogo.
    """
    response = requests.get(f"{API_URL_BOOKS}/livros/{id}")
    
    livro = response.json()
    livro['titulo'] = capitalize_first_letter(livro['titulo'])
    livro['descricao'] = capitalize_first_letter(livro['descricao']) + "."

    return render_template('livro.html', livro=livro)

# Página de recomendação
@router.route('/recomenda')
def recomenda():
    return render_template("recomenda.html")

# Página de administração de livros
@router.route("/admin/livros")
def pagina_admin():
    return render_template("admin/livros.html")