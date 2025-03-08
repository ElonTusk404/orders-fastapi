from datetime import timezone, datetime
from src.models import BaseModel
from sqlalchemy import DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship


class OrderModel(BaseModel):

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String) 
    status: Mapped[str] = mapped_column(String, default="pending")
    total: Mapped[int] = mapped_column(Integer, nullable=True)
    address: Mapped[str] = mapped_column(String, nullable=False)  
    city: Mapped[str] = mapped_column(String, nullable=False)    
    country: Mapped[str] = mapped_column(String, nullable=False) 
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    items: Mapped[list["OrderItemModel"]] = relationship("OrderItemModel", back_populates="order", lazy="subquery")


class OrderItemModel(BaseModel):

    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id", ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)  
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    order: Mapped["OrderModel"] = relationship("OrderModel", back_populates="items")