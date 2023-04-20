import os
import requests
import schedule
from dotenv import load_dotenv
import constants
from botUtils import check_revenue, check_app_status
from db.dbConfig import dbConfig

load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')


def direct_notification(message, chat_id):
    url = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s' % (
        f'{API_TOKEN}', f'{chat_id}')
    _ = requests.post(url, json={'text': f'{message}'}, timeout=10)


def apps_status_notification(bot, message):
    # get pkgs of the current user
    pkgs = dbConfig().get_pkgs(int(message.chat.id))
    # check if there is no pkgs
    if len(pkgs) <= 0:
        bot.send_message(message.chat.id, constants.YOU_HAVE_NO_APPS)
    # split apps checking around the hour
    every = int(60 * 60 / len(pkgs))
    for index, pkg in enumerate(pkgs, start=1):
        if not schedule.get_jobs(str(message.chat.id) + pkg):
            schedule.every(every * index).seconds.do(check_app_status, pkg, bot, message).tag(
                str(message.chat.id) + pkg)


def revenue_notification(bot, message):
    if not schedule.get_jobs(message.chat.id):
        schedule.every(1).day.at("07:00").do(check_revenue, bot, message).tag(message.chat.id)


def notifier(bot, message):
    revenue_notification(bot, message)
    apps_status_notification(bot, message)
