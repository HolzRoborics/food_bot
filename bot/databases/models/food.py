from sqlalchemy import Column, String, Numeric

from .. import Base
from .base import BaseMixin


class Food(BaseMixin, Base):
    name = Column(String(50))
    price = Column(Numeric(10, 2), nullable=False)
