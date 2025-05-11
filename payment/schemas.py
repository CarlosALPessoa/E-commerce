from pydantic import BaseModel

class PaymentRequest(BaseModel):
    amount: float
    payment_method: str

class PaymentResponse(BaseModel):
    message: str