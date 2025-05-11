from fastapi import APIRouter, Depends
from typing import List
from schema import SaleCreate, ProductItem
from model import Sale
from database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.orm.attributes import flag_modified
from fastapi import Query


import httpx
import json

router = APIRouter()

@router.post("/sales/")
async def create_sale(request: SaleCreate, db: Session = Depends(get_db)):
    book_id = request.book_id
    user_id = request.user_id

    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://127.0.0.1:8002/livros/{book_id}")

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Livro não foi encontrado no banco de dados.")
    
    data = response.json()

    try:
        item = {
            "prodct_id": data["id"],
            "prodct_title": data["titulo"],
            "prodct_price": data["preco"],
            "product_cat": data["categoria"]
        }


    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao validar o item: {e}")

    last_sale = db.query(Sale).filter(Sale.status_sale == "Pendente",Sale.user_id == user_id).order_by(Sale.id.desc()).first()

    if not last_sale:
        last_sale = Sale(
                        user_id=user_id,
                        items=[],
                        status_sale = "Pendente"
                    )  # <-- Define como lista vazia
        db.add(last_sale)
        db.commit()
        db.refresh(last_sale)

    items = last_sale.items or []
    items.append(item)

    last_sale.items = items
    flag_modified(last_sale, "items")
    print(last_sale.items)

    db.add(last_sale)
    db.commit()

    print(last_sale.status_sale)

    return {
        "message": "Item adicionado com sucesso.",
        "order_id": last_sale.id,
        "user_id": last_sale.user_id,
        "items": last_sale.items,
        "total": sum(i["prodct_price"] for i in last_sale.items)
    }

@router.post("/order_pay/{user_id}")
async def post_sale(user_id:int, db: Session=Depends(get_db)):
    last_sale = db.query(Sale).filter(Sale.status_sale == "Pendente",Sale.user_id == user_id).order_by(Sale.id.desc()).first()

    if not last_sale:
        return "O usuário não tem pedidos no carrinho."
    
    if last_sale.status_sale == "Pendente":
        last_sale.status_sale = "Concluido"
        flag_modified(last_sale, "status_sale")
        print(last_sale.items)

        db.add(last_sale)
        db.commit()

        print(last_sale.status_sale)

        return {
            "order_status": "Pedido feito com sucesso!"
        }
    else:
        return "Precisa realizar pedido."

@router.get("/get_cat/{user_id}")
async def get_cat(user_id:int, db: Session=Depends(get_db)):
    sales = db.query(Sale).filter(Sale.status_sale=="Concluido", Sale.user_id == user_id).order_by(Sale.id.desc()).all()

    if not sales:
        sales = None

    categorias = []
    
    if sales != None:
        for sale in sales:
            try:
                items_raw = sale.items

                # Converte se estiver em formato string
                if isinstance(items_raw, str):
                    items_raw = json.loads(items_raw)

                # Converte os itens para ProductItem
                items = [ProductItem(**item) for item in items_raw]

                for item in items:
                    if item.product_cat not in categorias:
                        categorias.append(item.product_cat)
            
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Erro ao processar categorias {sale.id}: {str(e)}"
                )
            
    last_sale = db.query(Sale).filter(Sale.status_sale == "Pendente",Sale.user_id == user_id).order_by(Sale.id.desc()).first()

    if not last_sale:
        last_sale = None
    
    if last_sale != None:
        for item in last_sale.items:
            if item["product_cat"] not in categorias:
                categorias.append(item["product_cat"])

    if categorias is None:
        raise HTTPException(
                    status_code=400,
                    detail=f"Usuário não possui histórico."
                )
    return categorias

@router.get("/order_pay/{user_id}")
async def get_order(user_id:int, db: Session=Depends(get_db)):
    sales = db.query(Sale).filter(Sale.status_sale == "Concluido",Sale.user_id == user_id).order_by(Sale.id.desc()).all()

    if not sales:
        return "O usuário não tem pedidos concluidos."
    
    result = []

    for sale in sales:
        try:
            items_raw = sale.items

            # Converte se estiver em formato string
            if isinstance(items_raw, str):
                items_raw = json.loads(items_raw)

            # Converte os itens para ProductItem
            items = [ProductItem(**item) for item in items_raw]

            total = sum(item.prodct_price for item in items)

            result.append({
                "Ordem do pedido": sale.id,
                "Itens Comprados": items,
                "Total da Compra": total
            })

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao processar venda {sale.id}: {str(e)}"
            )
    
    return result

@router.get("/cart/{user_id}") 
def get_sale(user_id: int, db: Session=Depends(get_db)):
    
    # Recuperando a última venda
    last_sale = db.query(Sale).filter(Sale.status_sale == "Pendente",Sale.user_id == user_id).order_by(Sale.id.desc()).first()

    if not last_sale:
        raise HTTPException(status_code=400, detail="Carrinho Vazio")
    
    print(f"Venda encontrada para o usuário {user_id}: {last_sale.id}")
    
    try:
        total = sum(item["prodct_price"] for item in last_sale.items)  # Verifique o nome do campo "prodct_price"
    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao acessar preço do produto: {str(e)}")

    return {
        "id": last_sale.id,
        "items": last_sale.items,
        "total": total 
    }




