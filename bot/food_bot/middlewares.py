from aiogram import types
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.emoji import emojize

from schemas import UserModel


class AuthMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get()

        try:
            user = await UserModel.get_user(message.from_user.id)
        except:
            await message.reply(text=emojize('Ваш ID не найден в базе:cry:'), reply=False)
            raise CancelHandler()
