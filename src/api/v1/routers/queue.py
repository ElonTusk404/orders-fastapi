from typing import Annotated
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from src.config import settings
from faststream.rabbit.fastapi import RabbitRouter, Logger
from src.schemas.queue import QueueOrderInfo
from src.api.v1.services import OrderService

router = RabbitRouter(settings.RABBITMQ)

class CartMessage(BaseModel):
    product_id: int
    quantity: int

def call():
    return True

def broker():
    return router.broker


@router.subscriber("order_items_reserved")
async def order_accepted(order_svc: Annotated[OrderService, Depends()], order_info: QueueOrderInfo, logger: Logger, d=Depends(call)):
    order_info.status='accepted'
    await order_svc.update_order(order_data=order_info)
    


@router.subscriber("order_items_unavailable")
async def order_accepted(order_svc: Annotated[OrderService, Depends()], order_info: QueueOrderInfo, logger: Logger, d=Depends(call), ):
    order_info.status='canceled'
    await order_svc.update_order(order_data=order_info)
