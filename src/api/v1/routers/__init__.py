__all__ = [
    'v1_cart_router',
    'v1_queue_router',
    'v1_order_router'
]

from src.api.v1.routers.cart import router as v1_cart_router
from src.api.v1.routers.queue import router as v1_queue_router
from src.api.v1.routers.order import router as v1_order_router