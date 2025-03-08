from src.models import CartModel, CartItemModel
from src.utils.repository import SqlAlchemyRepository


class CartRepository(SqlAlchemyRepository):
    model = CartModel

class CartItemRepository(SqlAlchemyRepository):
    model = CartItemModel

    