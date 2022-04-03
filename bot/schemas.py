from databases import Session, User
from pydantic import BaseModel
from sqlalchemy.future import select


class UserModel(BaseModel):
    # TODO user fields

    class Config:
        orm_mode = True

    @classmethod
    async def get_user(cls, user_id):
        async with Session() as session:
            stmt = select(User).where(User.id == user_id)
            result = await session.execute(stmt)
        user = result.scalars().first()
        return cls.from_orm(user)
