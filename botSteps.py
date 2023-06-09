import re
import constants
from db.dbConfig import dbConfig


def process_pkg_step(_message, _bot):
    if _message.text.strip() == '/cancel':
        return _bot.send_message(_message.chat.id, f'{constants.CANCEL}', parse_mode="HTML")
    pkg = _message.text.strip()
    chat_id = _message.chat.id
    if not re.match(r"^([A-Za-z]{1}[A-Za-z\d_]*\.)+[A-Za-z][A-Za-z\d_]*$", pkg):
        _bot.send_message(_message.chat.id, constants.PKG_NOT_VALID, parse_mode="HTML")
        return _bot.register_next_step_handler(message=_message, callback=process_pkg_step, _bot=_bot)
    if len(dbConfig().get_pkg(pkg)) > 0:
        return _bot.send_message(_message.chat.id, constants.APP_EXIST, parse_mode="HTML")
    dbConfig().add_pkg(pkg, chat_id)
    return _bot.send_message(_message.chat.id, constants.APP_ADDED, parse_mode="HTML")


def process_pkgs_step(_message, _bot):
    if _message.text.strip() == '/cancel':
        return _bot.send_message(_message.chat.id, f'{constants.CANCEL}', parse_mode="HTML")
    pkgs = _message.text.strip().split(',')
    chat_id = _message.chat.id
    for pkg in pkgs:
        pkg = pkg.strip()
        if pkg == "" or pkg == " ":
            continue
        if not re.match(r"^([A-Za-z]{1}[A-Za-z\d_]*\.)+[A-Za-z][A-Za-z\d_]*$", pkg):
            _bot.send_message(_message.chat.id, f'<b>{pkg}</b> {constants.MULTI_PKG_NOT_VALID}', parse_mode="HTML")
            continue
        if len(dbConfig().get_pkg(pkg)) > 0:
            _bot.send_message(_message.chat.id, f'<b>{pkg}</b> {constants.APP_EXIST}', parse_mode="HTML")
            continue
        dbConfig().add_pkg(pkg, chat_id)
        _bot.send_message(_message.chat.id, f'<b>{pkg}</b> {constants.MULTI_APP_ADDED}', parse_mode="HTML")
    _bot.send_message(_message.chat.id, f'<b>Done</b> - Operation finished', parse_mode="HTML")
