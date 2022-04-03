import logging
from collections import Counter
from urllib.parse import urlparse

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from settings import bot_settings, redis_settings

from .fsm import Form

logging.basicConfig(level=logging.INFO)

redis_conf = urlparse(redis_settings.URI)
storage = RedisStorage2(
    host=redis_conf.hostname,
    port=redis_conf.port,
    db=int((redis_conf.path or "0").strip("/")),
)

bot = Bot(token=bot_settings.TOKEN)
dp = Dispatcher(bot, storage=storage)


async def get_main_menu(state: FSMContext):
    actions = InlineKeyboardMarkup()
    actions.add(
        InlineKeyboardButton(text="Добавить позицию", callback_data="select_position")
    )
    async with state.proxy() as data:
        if data.get("basket"):
            actions.add(
                InlineKeyboardButton(text="Посмотреть корзину", callback_data="basket")
            )
            actions.add(
                InlineKeyboardButton(
                    text="Очистить корзину", callback_data="clear_basket"
                )
            )
            actions.add(
                InlineKeyboardButton(
                    text="Подтвердить заказ", callback_data="confirm_order"
                )
            )

    return actions


def basket_message(basket: list):
    counter = Counter(basket)
    return "\n".join(
        f"{position}, кол-во: {count}" for position, count in counter.items()
    )


@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await Form.start.set()
    menu = await get_main_menu(state)
    await message.reply("Выберите действие:", reply_markup=menu)


@dp.message_handler(commands=["start", "help"], state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    await Form.start.set()

    actions = await get_main_menu(state)

    await message.reply("Привет!", reply=False)
    await message.reply("Выбери действие:", reply=False, reply_markup=actions)


@dp.callback_query_handler(
    lambda call: call.data == "select_position", state=Form.start
)
async def handle_position(call: CallbackQuery):
    await Form.select.set()
    markup = InlineKeyboardMarkup()
    food_categories = ["шашлык", "машлык", "салат"]
    for category in food_categories:
        button = InlineKeyboardButton(
            text=category, callback_data=f"category/{category}"
        )
        markup.add(button)

    await bot.delete_message(
        chat_id=call.from_user.id, message_id=call.message.message_id
    )
    await call.message.reply(
        text=f"Выберите категорию:", reply_markup=markup, reply=False
    )


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


@dp.callback_query_handler(
    lambda call: call.data.startswith("category"), state=Form.select
)
async def handle_category(call: CallbackQuery):
    category = call.data.split("/")[-1]
    markup = InlineKeyboardMarkup()
    food_categories = {
        "шашлык": ["шашлык_1", "шашлык_2", "шашлык_3"],
        "машлык": ["машлык_1", "машлык_2", "машлык_3"],
        "салат": ["салат_1", "салат_2", "салат_3"],
    }
    for position in food_categories[category]:
        button = InlineKeyboardButton(
            text=position, callback_data=f"position/{position}"
        )
        markup.add(button)
    await bot.delete_message(
        chat_id=call.from_user.id, message_id=call.message.message_id
    )
    await call.message.reply(
        text=f"Выберите позицию:", reply_markup=markup, reply=False
    )


@dp.callback_query_handler(
    lambda call: call.data.startswith("position"), state=Form.select
)
async def handle_category(call: CallbackQuery, state: FSMContext):
    position = call.data.split("/")[-1]

    async with state.proxy() as data:
        if basket := data.get("basket"):
            basket.append(position)
            data["basket"] = basket
        else:
            data["basket"] = [position]

    await Form.start.set()
    actions = await get_main_menu(state)

    await bot.delete_message(
        chat_id=call.from_user.id, message_id=call.message.message_id
    )
    await call.message.reply(text=f"Добавлен {position}", reply=False)
    await call.message.reply(
        text=f"Выберите действие", reply_markup=actions, reply=False
    )


@dp.callback_query_handler(lambda call: call.data == "basket", state="*")
async def cmd_basket(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if basket := data.get("basket"):
            basket_content = basket_message(basket)
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
    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton(text="Заказ подтверждаю", callback_data="process_order")
    )
    markup.add(InlineKeyboardButton(text="Отмена", callback_data="back"))

    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id, message_id=call.message.message_id
    )
    async with state.proxy() as data:
        if basket := data.get("basket"):
            basket_content = basket_message(basket)
            await call.message.reply(
                text=f"Подтвердите заказ:\n{basket_content}",
                reply_markup=markup,
                reply=False,
            )
        else:
            menu = await get_main_menu(state)
            await call.message.reply(
                text="Ваша корзина пуста", reply_markup=menu, reply=False
            )


@dp.callback_query_handler(lambda call: call.data == "process_order", state="*")
async def process_order(call: CallbackQuery, state: FSMContext):
    # TODO SQL

    async with state.proxy() as data:
        if data.get("basket"):
            data["basket"] = []

    await state.finish()
    await bot.delete_message(
        chat_id=call.from_user.id, message_id=call.message.message_id
    )
    await call.message.reply(text="Заказ сделан", reply=False)


def main():
    executor.start_polling(dp, skip_updates=True)
