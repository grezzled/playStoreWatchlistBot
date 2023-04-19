import os
import schedule
from dotenv import load_dotenv
from telebot import *
from telebot.async_telebot import *
import constants
from botFactories import pkgs_factory, delpkg_factory
from botFilters import pkgsCallbackFilter, delPkgCallbackFilter
from botKeyboards import pkgs_keyboard, options_keyboard
from botNotifier import notifier
from botSteps import process_pkg_step, process_pkgs_step
from db.dbConfig import dbConfig, build_db
from botUtils import revenue_details, build_cmds, apps_status_cmd

load_dotenv()

build_db()

bot = TeleBot(token=os.getenv('API_TOKEN'))

build_cmds(bot, False)


@bot.message_handler(commands=['start'])
def cmd_start(message):
    print(f'Count of running jobs: {len(schedule.get_jobs())}')
    bot.send_message(chat_id=message.chat.id, text=constants.START, parse_mode='HTML')
    notifier(bot, message)


@bot.message_handler(commands=['addapp'])
def cmd_add_app(message):
    bot.send_message(message.chat.id, constants.ENTER_PKG_NAME, parse_mode='HTML')
    bot.register_next_step_handler(message=message, callback=process_pkg_step, _bot=bot)


@bot.message_handler(commands=['addapps'])
def cmd_add_apps(message):
    bot.send_message(message.chat.id, constants.ENTER_PKGS_NAMES, parse_mode='HTML')
    bot.register_next_step_handler(message=message, callback=process_pkgs_step, _bot=bot)


@bot.message_handler(commands=['myapps'])
def cmd_list_apps(message):
    pkgs = dbConfig().get_pkgs(int(message.chat.id))
    if len(pkgs) <= 0:
        bot.send_message(message.chat.id, constants.YOU_HAVE_NO_APPS, parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, constants.SELECT_APP, parse_mode='HTML', reply_markup=pkgs_keyboard(pkgs))


@bot.message_handler(commands=['statusapps'])
def status_pkgs(message):
    apps_status_cmd(bot, message)


@bot.message_handler(commands=['stopnotifier'])
def stop_notifier(message):
    schedule.clear()
    bot.send_message(message.chat.id, constants.NOTIFIER_STOPPED, parse_mode='HTML')


@bot.message_handler(commands=['revenue'])
def revenue(message):
    revenue_details(bot, message)


@bot.message_handler(commands=['startnotifier'])
def start_notifier(message):
    notifier(bot, message)
    bot.send_message(message.chat.id, constants.NOTIFIER_STARTED, parse_mode='HTML')


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


@bot.callback_query_handler(func=None, delpkg=delpkg_factory.filter())
def delpkg_callback(call: types.CallbackQuery):
    callback_data: dict = delpkg_factory.parse(callback_data=call.data)
    pkg = callback_data['pkg_id']
    dbConfig().del_pkg(pkg)
    bot.answer_callback_query(call.id, f'{pkg} deleted', show_alert=True)
    pkgs = dbConfig().get_pkgs(int(call.from_user.id))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=constants.SELECT_APP, parse_mode='HTML', reply_markup=pkgs_keyboard(pkgs))


@bot.message_handler(commands=['help'])
def cmd_help(message):
    bot.send_message(message.chat.id, constants.HELP_INSTRUCTIONS)


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")


bot.add_custom_filter(pkgsCallbackFilter())
bot.add_custom_filter(delPkgCallbackFilter())

# bot.infinity_polling()
if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)
