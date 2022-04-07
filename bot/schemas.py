from typing import List

from databases import Session, User, Food
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.engine import Result

from utils import food_filter
from settings import bot_settings


class UserModel(BaseModel):
    scud_id: int
    name: str
    telegram_id: int

    class Config:
        orm_mode = True

    @classmethod
    async def get_user(cls, telegram_id):
        async with Session() as session:
            stmt = select(User).where(User.telegram_id == telegram_id)
            result = await session.execute(stmt)
        user = result.scalars().first()
        return cls.from_orm(user)


class FoodModel(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        orm_mode = True

    @classmethod
    async def get_food(cls, food_id: int):
        async with Session() as session:
            stmt = select(Food).where(Food.id == food_id)
            result = await session.execute(stmt)
        return cls.from_orm(result.scalars().first())


class FoodList(BaseModel):
    __root__: List[FoodModel]

    def __len__(self):
        return len(self.__root__)

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]


class PaginatedList(BaseModel):
    all_items: FoodList
    current_page: int = 0
    items_per_page: int = bot_settings.ITEMS_PER_PAGE

    class Config:
        orm_mode = True

    @classmethod
    def from_db_result(cls, objects: Result) -> 'PaginatedList':
        foods = [FoodModel.from_orm(row) for row in objects.scalars()]
        filtered_foods = [food for food in foods if food_filter(food)]
        food_list = FoodList(__root__=filtered_foods)
        return cls(all_items=food_list)

    @property
    def _begin(self):
        return self.current_page * self.items_per_page

    @property
    def _end(self):
        return min((self.current_page + 1) * self.items_per_page, self.item_count)

    @property
    def item_count(self):
        return len(self.all_items)

    @property
    def page_items(self) -> List[FoodModel]:
        return self.all_items[self._begin: self._end]

    @property
    def current_page_number(self) -> int:
        return self.current_page + 1

    @property
    def has_next_page(self) -> bool:
        return self._end < self.item_count

    @property
    def has_previous_page(self) -> bool:
        return self._begin > 0

    def flip_next_page(self):
        self.current_page += 1

    def flip_previous_page(self):
        self.current_page -= 1
