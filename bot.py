import configparser
import logging
from datetime import datetime

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

path_file = "/tmp/photos/photo_%s.jpg"

# load configs
config = configparser.ConfigParser()
config.read('config.ini')
key = config['DEFAULT']['KEY']
userid = int(config['DEFAULT']['USERID'])


class BotAlbum():
    def __init__(self):
        self.pvs_dict = {}

    def hello(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Hello {}'.format(update.message.from_user.first_name))

    def save(self, update, context):
        if (update.message.from_user.id == userid):
            # -1 is the larger image
            new_file = update.message.photo[-1].bot.get_file(update.message.photo[-1].file_id)
            new_file.download(path_file % (str(datetime.now())))
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Miau miau, que bela fotinha, está\
                                     salva!")

        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Miau miau, que bela fotinha, mas \
                                     não vai ser salva!")



if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s -\
                        %(message)s', level=logging.INFO)

    updater = Updater(key, use_context=True)

    bot = BotAlbum()

    updater.dispatcher.add_handler(CommandHandler('hello', bot.hello))
    save_handler = MessageHandler(Filters.photo, bot.save)
    updater.dispatcher.add_handler(save_handler)
    updater.start_polling()
    updater.idle()
