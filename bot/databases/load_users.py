import asyncio
from pathlib import Path

import pandas
from databases import Session, User

package_dir = Path(__file__).parent.absolute()
file_path = package_dir.joinpath("users.xlsx")

sheet = pandas.read_excel(file_path, sheet_name=0)

users = []

for row in sheet.values.tolist():
    if not pandas.isna(row[3]):
        users.append(
            User(
                name=row[0],
                scud_id=int(row[2].replace(" ", "")),
                telegram_id=int(row[3]),
            )
        )


async def load_users():
    async with Session() as session:
        session.add_all(users)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(load_users())
