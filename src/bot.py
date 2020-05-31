from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from tinydb import TinyDB, Query
from config.auth import token
import logging

db = TinyDB('db.json')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('HabiticBot')

def start(update, context):
  logger.info('He recibido un comando start')
  chat_id=update.message.chat_id
  context.bot.send_message(
    chat_id,
    text="Hola soy habitic y vengo a ayudarte a crear habitos y organizar tu vida."
  )
  exist = db.search(Query().chat.id == chat_id)[0]
  if(exist):
    print('chatId exist: ' + str(exist['chat']['id']))
  else:
    db.insert({'chat': {'id': chat_id}})
    print('chatId: ' + str(chat_id))


def add(update, context):
  logger.info('He recibido un comando add')

def unknown(update, context):
  logger.info('He recibido un comando desconocido')
  context.bot.send_message(chat_id=update.message.chat_id, text="Lo siento, no me programaron para entender ese comando.")

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


if __name__ == '__main__':
  print('Iniciando bot')
  updater = Updater(token=token, use_context=True)
  dispatcher = updater.dispatcher

  dispatcher.add_handler(CommandHandler('start', start))
  dispatcher.add_handler(CommandHandler('add', add))
  dispatcher.add_handler(MessageHandler(Filters.command, unknown))
  dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

  updater.start_polling()
  updater.idle()