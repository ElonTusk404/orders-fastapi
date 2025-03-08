from typing import Annotated
from fastapi import status, APIRouter, Depends, HTTPException
from src.schemas.token import DecodedToken
from src.api.v1.services import CartService
from src.schemas.cart import CartResponse, AddToCartRequest
from src.utils.jwt import get_current_user
from src.api.v1.services import OrderService
from src.schemas.order import CreateOrderRequest, CreateOrderResponse
from src.schemas.queue import QueueOrderInfo
from src.api.v1.services import CartService

router = APIRouter(prefix='/orders', tags=['Заказы | v1'])



@router.post('', status_code=status.HTTP_202_ACCEPTED, response_model=QueueOrderInfo)
async def create_order(
    details: CreateOrderRequest,
    order_svc: Annotated[OrderService, Depends()],
    cart_svc: Annotated[CartService, Depends()],
    current_user: DecodedToken = Depends(get_current_user('write:orders')),
):
    
    order = await order_svc.create_order(user_id=current_user.user_id, details=details)
    await cart_svc.clear_cart(user_id=current_user.user_id)
    return order

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=CreateOrderResponse)
async def get_order(
    id: int,
    order_svc: Annotated[OrderService, Depends()],
    current_user: DecodedToken = Depends(get_current_user('read:orders'))
):
    return await order_svc.get_order(order_id=id, user_id=current_user.user_id)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    id: int,
    order_svc: Annotated[OrderService, Depends()],
    current_user: DecodedToken = Depends(get_current_user('delete:orders'))
):
    await order_svc.delete_order(order_id=id)

