from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from src.schemas.queue import QueueOrderInfo, QueueOrderItemInfo
class CreateOrderRequest(BaseModel):
    address: str
    city: str
    country: str
    phone_number: str


class OrderItemResponse(QueueOrderItemInfo):
    pass


class CreateOrderResponse(QueueOrderInfo):
    items: List[OrderItemResponse]



