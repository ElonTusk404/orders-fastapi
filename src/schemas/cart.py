from typing import List
from pydantic import BaseModel
from datetime import datetime




class AddToCartRequest(BaseModel):
    product_id: int
    quantity: int

class UpdateCartItemRequest(BaseModel):
    quantity: int

class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    created_at: datetime
    cart_id: int

class CartResponse(BaseModel):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime
    items: List[CartItemResponse]
