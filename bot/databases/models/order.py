from sqlalchemy import BigInteger, Column, ForeignKey, Integer, Date
from sqlalchemy.orm import relationship

from .. import Base
from .base import BaseMixin
from .food import Food
from .user import User


class Order(BaseMixin, Base):
    scud_id = Column(
        BigInteger, ForeignKey(User.scud_id, ondelete="CASCADE"), nullable=False
    )
    user = relationship(User)
    food_id = Column(Integer, ForeignKey(Food.id, ondelete="CASCADE"), nullable=False)
    food = relationship(Food)
    quantity = Column(Integer, nullable=False)
    datetime = Column(Date)
