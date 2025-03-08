from src.models import OrderModel, OrderItemModel
from src.utils.repository import SqlAlchemyRepository


class OrderRepository(SqlAlchemyRepository):
    model = OrderModel

class OrderItemRepository(SqlAlchemyRepository):
    model = OrderItemModel

    