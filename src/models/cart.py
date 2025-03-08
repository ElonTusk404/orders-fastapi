from datetime import timezone, datetime
from src.models import BaseModel
from sqlalchemy import DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship


class CartModel(BaseModel):

    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String, nullable=False)  
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    items: Mapped[list["CartItemModel"]] = relationship("CartItemModel", back_populates="cart", lazy="subquery")

class CartItemModel(BaseModel):

    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cart_id: Mapped[int] = mapped_column(Integer, ForeignKey("carts.id"))
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)  
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    cart: Mapped["CartModel"] = relationship("CartModel", back_populates="items")

