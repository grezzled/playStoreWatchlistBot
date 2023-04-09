from telebot import AdvancedCustomFilter, types
from telebot.callback_data import CallbackDataFilter


class pkgsCallbackFilter(AdvancedCustomFilter):
    key = 'config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


class delPkgCallbackFilter(AdvancedCustomFilter):
    key = 'delpkg'

    def check(self, call: types.CallbackQuery, delpkg: CallbackDataFilter):
        return delpkg.check(query=call)