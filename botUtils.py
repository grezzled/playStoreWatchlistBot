import os

import schedule
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


def _app_status_notifier(bot, message):
    pkgs = dbConfig().get_pkgs(int(message.chat.id))
    if len(pkgs) <= 0:
        bot.send_message(message.chat.id, constants.YOU_HAVE_NO_APPS)
    every = int(60 / len(pkgs))
    position = 1
    for pkg in pkgs:
        if not schedule.get_jobs(str(message.chat.id) + pkg):
            schedule.every(every * position).seconds.do(pkg_status_notifier, pkg, bot, message).tag(
                str(message.chat.id) + pkg)
        position += 1


def _max_revenue(bot, message):
    if not schedule.get_jobs(message.chat.id):
        schedule.every(30).minutes.do(revenue_notifier, bot, message).tag(message.chat.id)


def notifier(bot, message):
    _app_status_notifier(bot, message)
    _max_revenue(bot, message)


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


def status_notifier(bot, message) -> None:
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


def revenue_notifier(bot, message):
    alm = applovinMax(applovin_report_key)
    today_revenue = alm.today_revenue()
    yesterday_revenue = alm.yesterday_revenue()
    if today_revenue and yesterday_revenue:
        today_revenue = round(float(today_revenue), 2)
        yesterday_revenue = round(float(yesterday_revenue), 2)
    bot.send_message(message.chat.id, f'💰Yesterday💰: <b>{yesterday_revenue}$</b>'
                                      f' \n\n💰<b>Today</b>💰: <b>{today_revenue}$</b>',
                     parse_mode='HTML')
