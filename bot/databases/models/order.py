from sqlalchemy import BigInteger, Column, ForeignKey, Integer, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from .. import Base
from .food import Food
from .user import User


class Order(Base):
    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}"

    @declared_attr
    def id(cls):
        return Column(
            f"id", Integer, primary_key=True, index=True
        )
    order_id = Column(BigInteger, nullable=False)
    scud_id = Column(
        BigInteger, ForeignKey(User.scud_id, ondelete="CASCADE"), nullable=False
    )
    user = relationship(User)
    food_id = Column(Integer, ForeignKey(Food.id, ondelete="CASCADE"), nullable=False)
    food = relationship(Food)
    quantity = Column(Integer, nullable=False)
    datetime = Column(Date)
