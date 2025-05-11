from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from schemas import PaymentResponse, PaymentRequest
from database import get_db
from models import Payment

import requests
import traceback

router = APIRouter()

def verify_token(token: str):
    try:
        res = requests.get("http://127.0.0.1:3000/protected",
                           headers={"Authorization": f"Bearer {token}"})
        
        print(f"Token verification response: {res.status_code}")
        if res.status_code != 200:
            raise HTTPException(status_code=401, detail="Token inválido")
    except Exception as e:
        print(f"Erro ao verificar token: {e}")
        raise HTTPException(status_code=500, detail="Erro ao verificar token")

@router.post("/payment", response_model=PaymentResponse)
def create_payment(payment: PaymentRequest, db: Session = Depends(get_db), authorization: str = Header(...)):
    token = authorization.replace("Bearer", "").strip()
    verify_token(token)

    try:
        print(f"Recebendo pagamento com valor: {payment.amount} e método: {payment.payment_method}")

        new_payment = Payment(amount=payment.amount, method=payment.payment_method)
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)  # Caso queira retornar o pagamento recém-criado
        return PaymentResponse(message="Pagamento registrado com sucesso")
    except Exception as e:
        print(f"Erro ao salvar pagamento: {e}")
        db.rollback()  # Rollback em caso de erro
        raise HTTPException(status_code=500, detail="Erro ao registrar pagamento")
