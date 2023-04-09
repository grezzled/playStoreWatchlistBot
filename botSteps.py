from db.dbConfig import dbConfig


class botSteps:
    def __init__(self, bot, message):
        self._bot = bot
        self._message = message

    def process_pkg_step(self):
        # todo validate pkg name
        chat_id = self._message.chat.id
        pkg = self._message.text.strip()
        if len(dbConfig().get_pkg(pkg)) > 0:
            return self._bot.send_message(chat_id, 'App already exist')
        dbConfig().add_pkg(pkg, chat_id)
        self._bot.send_message(chat_id, 'App added successfully use command /myapps to see your apps')
