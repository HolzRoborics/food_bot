import logging
from collections import Counter
from urllib.parse import urlparse

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from aiogram.utils.emoji import emojize
from sqlalchemy.future import select

from databases import Session, Food, Order
from settings import bot_settings, redis_settings
from schemas import FoodModel, PaginatedList, UserModel

from .fsm import Form
from .keyboards import get_position_keyboard, get_confirmation_keyboard, get_main_menu
from .middlewares import AuthMiddleware

logging.basicConfig(level=logging.INFO)

redis_conf = urlparse(redis_settings.URI)
storage = RedisStorage2(
    host=redis_conf.hostname,
    port=redis_conf.port,
    db=int((redis_conf.path or "0").strip("/")),
)

bot = Bot(token=bot_settings.TOKEN)
dp = Dispatcher(bot, storage=storage)


async def basket_message(basket: list):
    counter = Counter(basket)
    messages = []
    sum_ = 0
    for position, count in counter.items():
        food = await FoodModel.get_food(position)
        sum_ += (food.price * count)
        messages.append(f"{food.name}, кол-во: {count}")
    messages.append(f'Сумма: {sum_}')
    return "\n".join(messages)


@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await Form.start.set()
    menu = await get_main_menu(state)
    await message.reply("Выбери действие:", reply_markup=menu)


@dp.message_handler(commands=["start", "help"], state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    await Form.start.set()

    async with Session() as session:
        stmt = select(Food)
        result = await session.execute(stmt)

    paginated_food = PaginatedList.from_db_result(result)

    async with state.proxy() as data:
        data['paginated_food'] = paginated_food.json()

    actions = await get_main_menu(state)

    await message.reply(emojize("Привет! Давай закажем еду?:poultry_leg:"), reply=False)
    await message.reply("Выбери действие:", reply=False, reply_markup=actions)


@dp.callback_query_handler(lambda call: call.data.startswith("back"), state='*')
async def cmd_back(call: CallbackQuery, state: FSMContext):
    await Form.start.set()

    actions = await get_main_menu(state)
    await bot.delete_message(
        chat_id=call.from_user.id, message_id=call.message.message_id
    )
    await call.message.reply("Выбери действие:", reply=False, reply_markup=actions)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


@dp.callback_query_handler(lambda call: call.data.startswith("select_position"), state=[Form.start, Form.select])
async def handle_category(call: CallbackQuery, state: FSMContext):
    page = call.data.split("/")[-1]

    await Form.select.set()

    async with state.proxy() as data:
        paginated_food = PaginatedList.parse_raw(data['paginated_food'])

    if page == 'next':
        paginated_food.flip_next_page()
    if page == 'previous':
        paginated_food.flip_previous_page()

    async with state.proxy() as data:
        data['paginated_food'] = paginated_food.json()

    kb = get_position_keyboard(paginated_food)

    await bot.delete_message(
        chat_id=call.from_user.id, message_id=call.message.message_id
    )

    await call.message.reply(
        text=f"Выберите позицию:", reply_markup=kb, reply=False
    )


@dp.callback_query_handler(lambda call: call.data.startswith("position"), state=Form.select)
async def handle_category(call: CallbackQuery, state: FSMContext):
    position = int(call.data.split("/")[-1])

    async with state.proxy() as data:
        if basket := data.get("basket"):
            basket.append(position)
            data["basket"] = basket
        else:
            data["basket"] = [position]

    await Form.start.set()
    actions = await get_main_menu(state)

    food = await FoodModel.get_food(position)

    await bot.delete_message(
        chat_id=call.from_user.id, message_id=call.message.message_id
    )
    await call.message.reply(text=f"Добавлен {food.name}", reply=False)
    await call.message.reply(
        text=f"Выбери действие:", reply_markup=actions, reply=False
    )


@dp.callback_query_handler(lambda call: call.data == "basket", state="*")
async def cmd_basket(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if basket := data.get("basket"):
            basket_content = await basket_message(basket)
            await call.message.reply(
                text=f"Ваша корзина:\n{basket_content}", reply=False
            )
        else:
            await call.message.reply(text="Ваша корзина пуста", reply=False)


@dp.callback_query_handler(lambda call: call.data == "clear_basket", state="*")
async def clear_basket(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data.get("basket"):
            data["basket"] = []
            await call.message.reply(text="Корзина очищена", reply=False)
        else:
            await call.message.reply(text="Ваша корзина пуста", reply=False)


@dp.callback_query_handler(lambda call: call.data == "confirm_order", state="*")
async def confirm_order(call: CallbackQuery, state: FSMContext):
    kb = get_confirmation_keyboard()

    await bot.delete_message(
        chat_id=call.from_user.id, message_id=call.message.message_id
    )
    async with state.proxy() as data:
        if basket := data.get("basket"):
            basket_content = await basket_message(basket)
            await call.message.reply(
                text=f"Подтвердите заказ:\n{basket_content}",
                reply_markup=kb,
                reply=False,
            )
        else:
            menu = await get_main_menu(state)
            await call.message.reply(
                text="Ваша корзина пуста", reply_markup=menu, reply=False
            )


@dp.callback_query_handler(lambda call: call.data == "process_order", state="*")
async def process_order(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data.get("basket"):
            basket = data.get("basket")
        else:
            return

    current_user = await UserModel.get_user(call.from_user.id)
    food_counter = Counter(basket)

    async with Session() as session:
        for food_id, qty in food_counter.items():
            session.add(Order(scud_id=current_user.scud_id,
                              food_id=food_id,
                              quantity=qty))
        await session.commit()

    await state.finish()
    await bot.delete_message(
        chat_id=call.from_user.id, message_id=call.message.message_id
    )
    await call.message.reply(text="Заказ сделан:", reply=False)
    message = await basket_message(basket)
    await call.message.reply(text=message, reply=False)


def main():
    # dp.setup_middleware(AuthMiddleware())
    executor.start_polling(dp, skip_updates=True)
