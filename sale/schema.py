from pydantic import BaseModel

class ProductItem(BaseModel):
    prodct_id: int
    prodct_title: str
    prodct_price: float
    product_cat: str

class SaleCreate(BaseModel):
    book_id: int
    user_id: int

class SaleResponse(BaseModel):
    id: int
    items: list[ProductItem]