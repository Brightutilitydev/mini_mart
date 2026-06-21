#!/usr/bin/env python3
"""Order Model"""

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel

class Order(BaseModel, Base):
    """Define an order and its properties"""

    __tablename__ = "orders"

    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    completed = Column(Integer, nullable=False, default=0)
    
    # --- NEW COLUMNS FOR DISPATCH ROUTING ---
    delivery_address = Column(String(255), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    gps_link = Column(String(255), nullable=True)

    user = relationship("User", back_populates="orders")
    order_items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )

    def __init__(self, *args, **kwargs):
        """Initialize the class"""
        if "completed" in kwargs:
            self.completed = kwargs.get("completed")
        else:
            self.completed = 0
            
        # Support the new data arriving from frontend kwargs
        if "delivery_address" in kwargs:
            self.delivery_address = kwargs.get("delivery_address")
        if "contact_phone" in kwargs:
            self.contact_phone = kwargs.get("contact_phone")
        if "gps_link" in kwargs:
            self.gps_link = kwargs.get("gps_link")
            
        super().__init__(*args, **kwargs)

    def to_dict(self):
        """Override to_dict to explicitly include order items in JSON responses"""
        order_dict = super().to_dict()
        
        # Explicitly grab the related items to send them to the React frontend
        if hasattr(self, 'order_items') and self.order_items is not None:
            order_dict['order_items'] = [item.to_dict() for item in self.order_items]
            
        return order_dict