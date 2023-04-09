import os
from telebot import *
from telebot.async_telebot import *
from telebot.callback_data import CallbackData, CallbackDataFilter
from db.dbConfig import dbConfig, build_db
from dotenv import load_dotenv
from scraper.gpScraper import scrap_app

load_dotenv()

sys.setrecursionlimit(1000)

API_TOKEN = os.getenv('API_TOKEN')


cmds = [
    telebot.types.BotCommand("myapps", "List your applications"),
    telebot.types.BotCommand("addapp", "Add an application"),
    telebot.types.BotCommand("status", "Return status of all apps"),
    telebot.types.BotCommand("start", "Welcoming message")
]

bot = TeleBot(API_TOKEN)

build_db()


bot.set_my_commands(cmds)


class pkgsCallbackFilter(AdvancedCustomFilter):
    key = 'config'

    def check(self, call: types.CallbackQuery, config: CallbackDataFilter):
        return config.check(query=call)


class delPkgCallbackFilter(AdvancedCustomFilter):
    key = 'delpkg'

    def check(self, call: types.CallbackQuery, delpkg: CallbackDataFilter):
        return delpkg.check(query=call)


pkgs_factory = CallbackData('pkg_id', prefix='pkgs')
delpkg_factory = CallbackData('pkg_id', prefix='delpkg')


def pkgs_keyboard(pkgs):
    return types.InlineKeyboardMarkup(
        row_width=1,
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text=pkg,
                    callback_data=pkgs_factory.new(pkg_id=pkg)
                )
            ] for pkg in pkgs
        ]
    )


def options_keyboard(pkg):
    return types.InlineKeyboardMarkup(
        row_width=2,
        keyboard=[
            [
                types.InlineKeyboardButton(
                    text='◀️ Go back to the list',
                    callback_data='back'
                )
            ], [
                types.InlineKeyboardButton(
                    text='🗑 Delete Application',
                    callback_data=delpkg_factory.new(pkg_id=pkg)
                )
            ]
        ]
    )


@bot.message_handler(commands=['myapps'])
def list_pkgs(message):
    print(message.chat.id)
    pkgs = dbConfig().get_pkgs(int(message.chat.id))
    if len(pkgs) <= 0:
        bot.send_message(message.chat.id, "You have no apps yet, please use the command /addapp the add a new app.")
    else:
        bot.send_message(message.chat.id, "Select an app to see the details", reply_markup=pkgs_keyboard(pkgs))


@bot.callback_query_handler(func=None, config=pkgs_factory.filter())
def pkgs_callback(call: types.CallbackQuery):
    callback_data: dict = pkgs_factory.parse(callback_data=call.data)
    pkg = callback_data['pkg_id']
    print(pkg)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=pkg, reply_markup=options_keyboard(pkg))


@bot.callback_query_handler(func=lambda c: c.data == 'back')
def back_callback(call: types.CallbackQuery):
    pkgs = dbConfig().get_pkgs(int(call.from_user.id))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Applications:', reply_markup=pkgs_keyboard(pkgs))


@bot.message_handler(commands=['addapp'])
def add_pkg(message):
    bot.send_message(message.chat.id, "Please enter your app package name")
    bot.register_next_step_handler(message, process_pkg_step)


def process_pkg_step(message):
    # todo validate pkg name
    chat_id = message.chat.id
    pkg = message.text.strip()
    if len(dbConfig().get_pkg(pkg)) > 0:
        return bot.send_message(message.chat.id, 'App already exist')
    dbConfig().add_pkg(pkg, chat_id)
    bot.send_message(message.chat.id, 'App added successfully use command /myapps to see your apps')


@bot.callback_query_handler(func=None, delpkg=delpkg_factory.filter())
def delpkg_callback(call: types.CallbackQuery):
    callback_data: dict = delpkg_factory.parse(callback_data=call.data)
    pkg = callback_data['pkg_id']
    dbConfig().del_pkg(pkg)
    bot.answer_callback_query(call.id, f'{pkg} deleted', show_alert=True)
    pkgs = dbConfig().get_pkgs(int(call.from_user.id))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Applications:', reply_markup=pkgs_keyboard(pkgs))


@bot.message_handler(commands=['status'])
def status_pkgs(message):
    pkgs = dbConfig().get_pkgs(int(message.chat.id))
    if len(pkgs) <= 0:
        bot.send_message(message.chat.id, "You have no apps yet, please use the command /addapp the add a new app.")
    else:
        for pkg in pkgs:
            if scrap_app(pkg, message.chat.id) is not False:
                bot.send_message(message.chat.id, f'🟢 {pkg}')
            else:
                bot.send_message(message.chat.id, f'🔴 {pkg}')


bot.add_custom_filter(pkgsCallbackFilter())
bot.add_custom_filter(delPkgCallbackFilter())
bot.infinity_polling()
