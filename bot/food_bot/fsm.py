from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    start = State()
    select = State()
    confirmation = State()
