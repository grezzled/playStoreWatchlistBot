from telebot import types

from botFactories import pkgs_factory, delpkg_factory


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