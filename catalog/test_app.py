import json
import random
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ---------- FIXTURES ----------

@pytest.fixture(scope="module")
def livros_data():
    """Carrega os dados de livros a partir de um arquivo JSON"""
    with open("livros.json", "r", encoding="utf-8") as file:
        return json.load(file)

@pytest.fixture(scope="module")
def created_livros_ids(livros_data):
    """Cria livros temporários na API e retorna a lista de IDs"""
    ids = []
    for livro in livros_data:
        response = client.post("/livros", json=livro)
        assert response.status_code in (200, 201), f"Erro ao criar livro: {livro['titulo']}"
        ids.append(response.json()["id"])
    return ids

# ---------- TESTES ----------

def test_criacao_livros(created_livros_ids):
    """Verifica se os livros foram criados e os IDs são únicos"""
    assert created_livros_ids, "Nenhum livro foi criado"
    assert len(created_livros_ids) == len(set(created_livros_ids)), "IDs duplicados encontrados"

def test_consulta_livro_aleatorio(created_livros_ids):
    """Consulta um livro aleatório e valida os dados"""
    random_id = random.choice(created_livros_ids)
    response = client.get(f"/livros/{random_id}")
    assert response.status_code == 200, f"Falha ao consultar o livro com ID {random_id}"

    livro = response.json()
    assert livro["id"] == random_id, f"ID retornado {livro['id']} não bate com o solicitado {random_id}"

def test_estrutura_resposta_livro(created_livros_ids):
    """Valida se a estrutura de resposta do livro contém todos os campos esperados"""
    response = client.get(f"/livros/{created_livros_ids[0]}")
    livro = response.json()

    campos_esperados = {
        "id": int,
        "titulo": str,
        "descricao": str,
        "preco": float,
        "image": str,
        "categoria": str,
        "qtd": int,
    }

    for campo, tipo in campos_esperados.items():
        assert campo in livro, f"Campo '{campo}' ausente na resposta"
        assert isinstance(livro[campo], tipo), f"Tipo incorreto em '{campo}': esperado {tipo}, recebido {type(livro[campo])}"

def test_consulta_livro_inexistente():
    """Verifica se a API responde corretamente ao buscar um ID inexistente"""
    num = 9999999
    response = client.get(f"/livros/{num}")
    assert response.status_code == 404, "Deveria retornar 404 para livro inexistente"
    assert "detail" in response.json(), "A resposta de erro deveria conter o campo 'detail'"
    return

