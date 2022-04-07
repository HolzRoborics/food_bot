import asyncio
from pathlib import Path

import pandas
from databases import Session, Food

# package_dir = Path(__file__).parent.absolute()
# file_path = package_dir.joinpath("food.xlsx")

sheet = pandas.read_excel("food.xlsx", sheet_name=0)

food = []

for row in sheet.values.tolist():
    food.append(Food(
        name=row[0], id=row[1], price=row[2]
    )
    )


async def load_food():
    async with Session() as session:
        session.add_all(food)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(load_food())
