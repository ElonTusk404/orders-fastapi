from pydantic import BaseModel

from typing import Optional, List
from datetime import datetime
class QueueOrderItemInfo(BaseModel):
    id: int
    product_id: int
    quantity: int
    order_id: int

    class Config:
        from_attributes = True

class QueueOrderInfo(BaseModel):
    id: int
    status: str
    total: Optional[int] = None
    address: str
    city: str
    country: str
    phone_number: str
    created_at: datetime
    updated_at: datetime
    items: List[QueueOrderItemInfo]

    class Config:
        from_attributes = True