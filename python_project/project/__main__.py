import time
import asyncio
from databases import Session, User
from sqlalchemy.future import select


async def main():
    async with Session() as session:
        user = User(name='John Snow')
        session.add(user)
        await session.commit()
    while True:
        async with Session() as session:
            stmt = select(User)
            result = await session.execute(stmt)
            user = result.scalars().first()
            print(f"Получен пользователь из бд {user.name}")
        time.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
