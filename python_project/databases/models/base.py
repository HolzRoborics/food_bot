from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr


class BaseMixin:
    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}"

    @declared_attr
    def id(cls):
        return Column(
            f"{cls.__name__.lower()}_id", Integer, primary_key=True, index=True
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.id}{': ' + getattr(self, 'name') if hasattr(self, 'name') else ''}>"

    __str__ = __repr__
