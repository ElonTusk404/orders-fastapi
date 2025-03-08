from fastapi import HTTPException, status
from src.models import CartModel, OrderModel
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode
from src.schemas.order import CreateOrderRequest, CreateOrderResponse
from src.schemas.queue import QueueOrderInfo

class OrderService(BaseService):
    base_repository: str = 'order'


    @transaction_mode
    async def create_order(self, user_id: str, details: CreateOrderRequest):
        from src.api.v1.routers.queue import broker 

        cart : CartModel = await self.uow.cart.get_by_query_one_or_none(user_id=user_id)
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart not found"
            )
        if not cart.items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart is empty"
            )
        
        order: OrderModel = await self.uow.order.add_one_and_get_obj(user_id=user_id, **details.model_dump(exclude_none=True))

        for item in cart.items:
            await self.uow.order_item.add_one(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity
            )
        full_order : OrderModel = await self.uow.order.get_by_query_one_or_none(id=order.id)
        order_pydantic = QueueOrderInfo.model_validate(full_order)
        
        await broker().publish(
            queue='order_created',
            message=order_pydantic
        )
        
        return full_order

    @transaction_mode
    async def update_order(self, order_data: QueueOrderInfo):
        await self.uow.order.update_one_by_id(
            obj_id=order_data.id, status = order_data.status, total = order_data.total
        )
    

    @transaction_mode
    async def get_order(self, order_id: int, user_id: int) -> CreateOrderResponse:
        order = await self.uow.order.get_by_query_one_or_none(id = order_id, user_id = user_id)
        if order:
            return order
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
         
    @transaction_mode
    async def delete_order(self, order_id: int)-> None:
        order = await self.uow.order.get_by_query_one_or_none(id = order_id)
        if order:
            await self.uow.order.delete_by_query(id = order_id)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)