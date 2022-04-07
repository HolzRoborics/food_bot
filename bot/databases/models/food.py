from sqlalchemy import Column, Numeric, String, Integer, ForeignKey

from .. import Base
from .base import BaseMixin


class FoodCategory(BaseMixin, Base):
    name = Column(String(50))


class Food(BaseMixin, Base):
    name = Column(String(50))
    price = Column(Numeric(10, 2), nullable=False)
    category_id = Column(Integer, ForeignKey(FoodCategory.id, ondelete="CASCADE"))
