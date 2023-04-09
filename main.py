import os
import schedule
from dotenv import load_dotenv
from telebot import *
from telebot.async_telebot import *
from botFactories import pkgs_factory, delpkg_factory
from botFilters import pkgsCallbackFilter, delPkgCallbackFilter
from botKeyboards import pkgs_keyboard, options_keyboard
from botSteps import botSteps
from db.dbConfig import dbConfig, build_db
from scraper.gpScraper import scrap_app

""" Load environment variables """
load_dotenv()

""" Create database and it's tables if it's not already created """
build_db()

""" Initialize the bot commands """
# cmds = [
#     telebot.types.BotCommand("start", "Welcoming message"),
#     telebot.types.BotCommand("myapps", "Get a list of your apps"),
#     telebot.types.BotCommand("addapp", "Add an app to your list"),
#     telebot.types.BotCommand("delapp", "Delete an app"),
#     telebot.types.BotCommand("status", "Return status of your apps"),
#     telebot.types.BotCommand("cancel", "cancel the current operation"),
# ]
# bot.set_my_commands(cmds)


bot = TeleBot(token=os.getenv('API_TOKEN'))


@bot.message_handler(commands=['myapps'])
def list_pkgs(message):
    pkgs = dbConfig().get_pkgs(int(message.chat.id))
    if len(pkgs) <= 0:
        bot.send_message(message.chat.id,
                         "You have no apps yet, please use the command <b>/addapp</b> the add a new app.",
                         parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, "<b>Select an app to see the details</b>", parse_mode='HTML',
                         reply_markup=pkgs_keyboard(pkgs))


@bot.callback_query_handler(func=None, config=pkgs_factory.filter())
def pkgs_callback(call: types.CallbackQuery):
    callback_data: dict = pkgs_factory.parse(callback_data=call.data)
    pkg = callback_data['pkg_id']
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
    status_notifier(chat_id=message.chat.id)


def status_notifier(chat_id) -> None:
    pkgs = dbConfig().get_pkgs(int(chat_id))
    if len(pkgs) <= 0:
        bot.send_message(chat_id, "You have no apps yet, please use the command /addapp the add a new app.")
    else:
        for pkg in pkgs:
            if scrap_app(pkg, chat_id) is not False:
                bot.send_message(chat_id, f'🟢 {pkg}')
            else:
                bot.send_message(chat_id, f'🔴 {pkg}')


@bot.message_handler(commands=['start'])
def set_timer(message):
    bot.send_message(chat_id=message.chat.id,
                     text='Hi! welcome to our bot, check /help to get all the information about how to use our bot')
    schedule.every(random.randrange(3600, 7200)).seconds.do(status_notifier, message.chat.id).tag(message.chat.id)


@bot.message_handler(commands=['unset'])
def unset_timer(message):
    schedule.clear(message.chat.id)


bot.add_custom_filter(pkgsCallbackFilter())
bot.add_custom_filter(delPkgCallbackFilter())
# bot.infinity_polling()
if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)
