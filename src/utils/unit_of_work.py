"""The module contains base classes for supporting transactions."""

import functools
from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any, Never

from src.database.db import async_session_maker
from src.repositories.cart import CartRepository, CartItemRepository
from src.repositories.order import OrderRepository, OrderItemRepository
from src.utils.custom_types import AsyncFunc


class AbstractUnitOfWork(ABC):

    @abstractmethod
    def __init__(self) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> Never:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> Never:
        raise NotImplementedError


class UnitOfWork(AbstractUnitOfWork):
    """The class responsible for the atomicity of transactions."""

    def __init__(self) -> None:
        self.session_factory = async_session_maker

    async def __aenter__(self) -> None:
        self.session = self.session_factory()
        self.cart = CartRepository(self.session)
        self.cart_item = CartItemRepository(self.session)
        self.order = OrderRepository(self.session)
        self.order_item = OrderItemRepository(self.session)

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if not exc_type:
            await self.commit()
        else:
            await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()


from functools import wraps
from typing import Callable, TypeVar, ParamSpec, Any, cast
import asyncio

P = ParamSpec("P")  
R = TypeVar("R")   

def transaction_mode(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    async def wrapper(self: Any, *args: P.args, **kwargs: P.kwargs) -> R:
        if not hasattr(self, "uow"):
            raise AttributeError("Объект должен иметь атрибут 'uow' для работы с транзакцией")
        
        async with self.uow:
            result = await func(self, *args, **kwargs)
            return result
            

    return cast(Callable[P, R], wrapper)