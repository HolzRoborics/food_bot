from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.emoji import emojize


def get_position_keyboard(paginated_food):
    arrows = []
    if paginated_food.has_previous_page:
        arrows.append(InlineKeyboardButton(
            text=emojize(':arrow_backward:'), callback_data=f"select_position/previous"
        ))
    if paginated_food.has_next_page:
        arrows.append(InlineKeyboardButton(
            text=emojize(':arrow_forward:'), callback_data=f"select_position/next"
        ))
    buttons = [*[[InlineKeyboardButton(
        text=f'{position.name} - {position.price} руб', callback_data=f"position/{position.id}"
    )] for position in paginated_food.page_items] + [arrows]]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_confirmation_keyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Заказ подтверждаю", callback_data="process_order"),
                                                    InlineKeyboardButton(text="Отмена", callback_data="back")]])
    return kb


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