from sqlalchemy import Column, Numeric, String

from .. import Base
from .base import BaseMixin


class Food(BaseMixin, Base):
    name = Column(String(50))
    price = Column(Numeric(10, 2), nullable=False)
