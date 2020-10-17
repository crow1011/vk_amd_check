import telebot
from get_config import get_tg_config, get_logger_config
from get_logger import get_logger

tg_conf = get_tg_config()
logger_conf = get_logger_config()
logger = get_logger(logger_conf)
bot = telebot.TeleBot(tg_conf['api_key'])


@bot.message_handler(commands=['my_id', 'get_my_id'])
def my_id(message):
    try:
        bot.send_message(message.chat.id, 'Sending your chat id...')
        bot.send_message(message.chat.id, str(message.chat.id))
        bot.send_message(message.chat.id, '...Done')
    except Exception:
        logger.exception('# Exception')

bot.polling()
