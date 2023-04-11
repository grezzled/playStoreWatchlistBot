import os
import schedule
from dotenv import load_dotenv
from telebot import *
from telebot.async_telebot import *
from telebot.handler_backends import StatesGroup

import constants
from botFactories import pkgs_factory, delpkg_factory
from botFilters import pkgsCallbackFilter, delPkgCallbackFilter
from botKeyboards import pkgs_keyboard, options_keyboard
from botSteps import process_pkg_step, process_pkgs_step
from db.dbConfig import dbConfig, build_db
from scraper.gpScraper import scrap_app

from api.applovinMax import applovinMax

""" Load environment variables """
load_dotenv()

""" Create database and it's tables if it's not already created """
build_db()

""" Initialize the bot commands """
cmds = [
    telebot.types.BotCommand("start", "Welcoming message"),
    telebot.types.BotCommand("addapp", "Add an app"),
    telebot.types.BotCommand("addapps", "Add multiple apps at once"),
    telebot.types.BotCommand("myapps", "Show the list of your apps"),
    telebot.types.BotCommand("statusapps", "Check status of your apps"),
    telebot.types.BotCommand("cancel", "Cancel the current operation"),
    telebot.types.BotCommand("startnotifier", "Turn on notifications to receive updates"),
    telebot.types.BotCommand("stopnotifier", "Turn off notifications to stop receiving updates"),
    telebot.types.BotCommand("help", "Instructions for using Bot commands"),

]

applovin_report_key = os.getenv('APPLOVIN_REPORT_KEY')

bot = TeleBot(token=os.getenv('API_TOKEN'))

bot.set_my_commands(cmds)


@bot.message_handler(commands=['start'])
def start(message):
    print(f'Count of running jobs: {len(schedule.get_jobs())}')
    bot.send_message(chat_id=message.chat.id, text=constants.START, parse_mode='HTML')
    notifier(message)


@bot.message_handler(commands=['addapp'])
def add_pkg(message):
    bot.send_message(message.chat.id, constants.ENTER_PKG_NAME, parse_mode='HTML')
    bot.register_next_step_handler(message=message, callback=process_pkg_step, _bot=bot)


@bot.message_handler(commands=['addapps'])
def add_pkgs(message):
    bot.send_message(message.chat.id, constants.ENTER_PKGS_NAMES, parse_mode='HTML')
    bot.register_next_step_handler(message=message, callback=process_pkgs_step, _bot=bot)


@bot.message_handler(commands=['myapps'])
def list_pkgs(message):
    pkgs = dbConfig().get_pkgs(int(message.chat.id))
    if len(pkgs) <= 0:
        bot.send_message(message.chat.id, constants.YOU_HAVE_NO_APPS, parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, constants.SELECT_APP, parse_mode='HTML', reply_markup=pkgs_keyboard(pkgs))


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
                          text=constants.YOUR_APPLICATIONS, parse_mode='HTML', reply_markup=pkgs_keyboard(pkgs))


@bot.message_handler(commands=['addapps'])
def add_pkg(message):
    bot.send_message(message.chat.id, "Please enter your apps package names separated by a comma (,)")
    bot.register_next_step_handler(message=message, callback=process_pkg_step, _bot=bot)


@bot.callback_query_handler(func=None, delpkg=delpkg_factory.filter())
def delpkg_callback(call: types.CallbackQuery):
    callback_data: dict = delpkg_factory.parse(callback_data=call.data)
    pkg = callback_data['pkg_id']
    dbConfig().del_pkg(pkg)
    bot.answer_callback_query(call.id, f'{pkg} deleted', show_alert=True)
    pkgs = dbConfig().get_pkgs(int(call.from_user.id))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=constants.SELECT_APP, parse_mode='HTML', reply_markup=pkgs_keyboard(pkgs))


@bot.message_handler(commands=['statusapps'])
def status_pkgs(message):
    status_notifier(chat_id=message.chat.id)


@bot.message_handler(commands=['help'])
def status_pkgs(message):
    bot.send_message(message.chat.id, constants.HELP_INSTRUCTIONS)


@bot.message_handler(commands=['stopnotifier'])
def stop_notifier(message):
    schedule.clear(message.chat.id)
    bot.send_message(message.chat.id, constants.NOTIFIER_STOPPED, parse_mode='HTML')


@bot.message_handler(commands=['startnotifier'])
def start_notifier(message):
    notifier(message)
    bot.send_message(message.chat.id, constants.NOTIFIER_STARTED, parse_mode='HTML')


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")


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


def revenue_notifier(chat_id):
    today_revenue = round(float(applovinMax(applovin_report_key).today_revenue()), 2)
    yesterday_revenue = round(float(applovinMax(applovin_report_key).yesterday_revenue()), 2)
    bot.send_message(chat_id, f'💰Yesterday💰: <b>{yesterday_revenue}$</b>'
                              f' \n\n💰<b>Today</b>💰: <b>{today_revenue}$</b>',
                     parse_mode='HTML')


def notifier(message):
    if not schedule.get_jobs(message.chat.id):
        schedule.every(1).hour.do(status_notifier, message.chat.id).tag(message.chat.id)
        schedule.every(3).seconds.do(revenue_notifier, message.chat.id).tag(message.chat.id)


bot.add_custom_filter(pkgsCallbackFilter())
bot.add_custom_filter(delPkgCallbackFilter())

# bot.infinity_polling()
if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)
