from sqlalchemy import Column, String, BigInteger

from .. import Base


class User(Base):
    __tablename__ = 'user'
    scud_id = Column(BigInteger, nullable=False, index=True, primary_key=True)
    name = Column(String(100))
    telegram_id = Column(BigInteger, nullable=False, index=True)
