from sqlalchemy import Column, Integer, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from .. import Base
from .base import BaseMixin
from .user import User
from .food import Food


class Order(BaseMixin, Base):
    scud_id = Column(BigInteger, ForeignKey(User.scud_id, ondelete='CASCADE'), nullable=False)
    user = relationship(User)
    food_id = Column(Integer, ForeignKey(Food.id, ondelete='CASCADE'), nullable=False)
    food = relationship(Food)
    quantity = Column(Integer, nullable=False)
