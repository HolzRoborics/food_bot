from sqlalchemy import Column, String

from .. import Base
from .base import BaseMixin


class User(BaseMixin, Base):
    name = Column(String(50))
