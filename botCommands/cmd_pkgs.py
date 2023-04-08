from telebot import types
from telebot.asyncio_filters import AdvancedCustomFilter
from telebot.callback_data import CallbackData, CallbackDataFilter
from telebot.types import InlineKeyboardButton
from db.dbConfig import dbConfig
from telebot.async_telebot import AsyncTeleBot


class PkgsCallbackFilter(AdvancedCustomFilter):
    key = 'config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


class cmd_pkgs:
    bot: AsyncTeleBot

    def __init__(self, bot: AsyncTeleBot):
        self.bot = bot
        bot.add_custom_filter(PkgsCallbackFilter())

    pkgs_factory = CallbackData('pkg_id', prefix='pkgs')

    def pkgs_keyboard(self, pkgs):
        return types.InlineKeyboardMarkup(
            row_width=1,
            keyboard=[
                [
                    types.InlineKeyboardButton(
                        text=pkg,
                        callback_data=self.pkgs_factory.new(pkg_id=pkg)
                    )
                ] for pkg in pkgs
            ]
        )

    async def list_pkgs(self, message):
        pkgs = dbConfig().get_pkgs(int(message.chat.id))
        await self.bot.send_message(message.chat.id, "Select PKG", reply_markup=self.pkgs_keyboard(pkgs))

    async def pkgs_callback(self, call: types.CallbackQuery):
        print(call)
        callback_data: dict = self.pkgs_factory.parse(callback_data=call.data)
        pkg_id = callback_data['pkg_id']

    async def add_pkg(self, message):
        pass
