from typing import Annotated
from fastapi import status, APIRouter, Depends, HTTPException
from src.schemas.token import DecodedToken
from src.api.v1.services import CartService
from src.schemas.cart import CartResponse, AddToCartRequest
from src.utils.jwt import get_current_user

router = APIRouter(prefix='/carts', tags=['Корзина | v1'])

@router.post('/items', status_code=status.HTTP_201_CREATED)
async def add_product_to_cart(
    data: AddToCartRequest,
    user: Annotated[DecodedToken, Depends(get_current_user('write:carts'))],
    service: Annotated[CartService, Depends()]
):
    await service.add_product_to_cart(user_id=user.user_id, data=data)

@router.delete('/items/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_product_from_cart(
    product_id: int,
    user: Annotated[DecodedToken, Depends(get_current_user("write:carts"))],
    service: Annotated[CartService, Depends()]
):
    await service.remove_product_from_cart(user_id=user.user_id, product_id=product_id)

@router.delete('/items', status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(
    user: Annotated[DecodedToken, Depends(get_current_user("write:carts"))],
    service: Annotated[CartService, Depends()]
):
    await service.clear_cart(user_id=user.user_id)

@router.get('/items', response_model=CartResponse, status_code=status.HTTP_200_OK)
async def get_user_cart(
    user: Annotated[DecodedToken, Depends(get_current_user('read:carts'))],
    service: Annotated[CartService, Depends()]
):
    return await service.get_user_cart(user_id=user.user_id)