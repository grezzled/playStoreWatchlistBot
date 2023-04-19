import os
import telebot
import constants
from api.applovinMax import applovinMax
from db.dbConfig import dbConfig
from scraper.gpScraper import scrap_app

applovin_report_key = os.getenv('APPLOVIN_REPORT_KEY')

cmds = [
    telebot.types.BotCommand("start", "Welcoming message"),
    telebot.types.BotCommand("addapp", "Add an app"),
    telebot.types.BotCommand("addapps", "Add multiple apps at once"),
    telebot.types.BotCommand("myapps", "Show the list of your apps"),
    telebot.types.BotCommand("statusapps", "Check status of your apps"),
    telebot.types.BotCommand("startnotifier", "Turn on notifications to receive updates"),
    telebot.types.BotCommand("stopnotifier", "Turn off notifications to stop receiving updates"),
    telebot.types.BotCommand("cancel", "Cancel the current operation"),
    telebot.types.BotCommand("revenue", "Get details about your revenue"),
    telebot.types.BotCommand("help", "Instructions for using Bot commands"),
]


def build_cmds(bot, debug=False):
    if debug:
        bot.set_my_commands(cmds)


def check_app_status(pkg, bot, message):
    if scrap_app(pkg, message.chat.id) is False:
        bot.send_message(message.chat.id, f'🔴 Alert: App is down ({pkg})')


def check_revenue(bot, message):
    alm = applovinMax(applovin_report_key)
    today_revenue = alm.today_revenue()
    yesterday_revenue = alm.yesterday_revenue()
    if today_revenue and yesterday_revenue:
        today_revenue = round(float(today_revenue), 2)
        yesterday_revenue = round(float(yesterday_revenue), 2)
    bot.send_message(message.chat.id, f'💰Yesterday💰: <b>{yesterday_revenue}$</b>'
                                      f' \n\n💰<b>Today</b>💰: <b>{today_revenue}$</b>',
                     parse_mode='HTML')


def revenue_details(bot, message):
    _msg = bot.send_message(chat_id=message.chat.id, text='Loading...', parse_mode='HTML')
    alm = applovinMax(applovin_report_key)
    today_revenue = alm.today_revenue()
    yesterday_revenue = alm.yesterday_revenue()
    if today_revenue and yesterday_revenue:
        today_revenue = round(float(today_revenue), 2)
        yesterday_revenue = round(float(yesterday_revenue), 2)
    bot.edit_message_text(chat_id=message.chat.id, message_id=_msg.message_id,
                          text=f'💰Yesterday💰: <b>{yesterday_revenue}$</b>'
                               f' \n\n💰<b>Today</b>💰: <b>{today_revenue}$</b>',
                          parse_mode='HTML')


def apps_status_cmd(bot, message) -> None:
    pkgs = dbConfig().get_pkgs(int(message.chat.id))
    if len(pkgs) <= 0:
        bot.send_message(message.chat.id, constants.YOU_HAVE_NO_APPS)
    else:
        for pkg in pkgs:
            if scrap_app(pkg, message.chat.id) is not False:
                bot.send_message(message.chat.id, f'🟢 {pkg}')
            else:
                bot.send_message(message.chat.id, f'🔴 {pkg}')


def pkg_status_notifier(pkg: str, bot, message):
    pkgs = dbConfig().get_pkg_by_user_id(pkg, int(message.chat.id))
    if len(pkgs) <= 0:
        bot.send_message(message.chat.id, constants.YOU_HAVE_NO_APPS)
    if pkg:
        if scrap_app(pkg, message.chat.id) is not False:
            bot.send_message(message.chat.id, f'🟢 {pkg}')
        else:
            bot.send_message(message.chat.id, f'🔴 {pkg}')
