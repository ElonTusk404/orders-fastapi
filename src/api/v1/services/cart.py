
from fastapi import HTTPException, status
from src.models import CartItemModel, CartModel
from src.schemas.cart import AddToCartRequest
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode

class CartService(BaseService):
    base_repository: str = 'cart'

    @transaction_mode
    async def add_product_to_cart(self, user_id: str, data: AddToCartRequest) -> None:

        cart = await self._get_or_create_user_cart(user_id)
        
        existing_item: CartItemModel = await self.uow.cart_item.get_by_query_one_or_none(
            cart_id=cart.id,
            product_id=data.product_id
        )

        if existing_item:
            new_quantity = existing_item.quantity + data.quantity
            await self.uow.cart_item.update_one_by_id(
                obj_id=existing_item.id,
                quantity=new_quantity
            )
        else:
            await self.uow.cart_item.add_one(
                cart_id=cart.id,
                product_id=data.product_id,
                quantity=data.quantity
            )

    @transaction_mode
    async def remove_product_from_cart(self, user_id: str, product_id: int) -> None:
        cart : CartModel = await self.get_user_cart(user_id)
        
        cart_item : CartItemModel = await self.uow.cart_item.get_by_query_one_or_none(
            cart_id=cart.id,
            product_id=product_id
        )
        
        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found in cart"
            )

        await self.uow.cart_item.delete_by_query(id=cart_item.id)

    @transaction_mode
    async def clear_cart(self, user_id: str) -> None:
        cart: CartModel = await self.get_user_cart(user_id)
        await self.uow.cart_item.delete_by_query(cart_id=cart.id)

    @transaction_mode
    async def get_user_cart(self, user_id: str) -> CartModel:
        cart : CartModel = await self.uow.cart.get_by_query_one_or_none(user_id=user_id)
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart not found"
            )
        return cart

    async def _get_or_create_user_cart(self, user_id: str) -> CartModel:
        cart = await self.uow.cart.get_by_query_one_or_none(user_id=user_id)
        if not cart:
            return await self.uow.cart.add_one_and_get_obj(user_id=user_id)
        return cart