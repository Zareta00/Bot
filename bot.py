import telebot
from config import keys, TOKEN
from utils import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def info(message: telebot.types.Message):
    text = 'Чтобы узнать курс валюты введите название валюты. \nЧтобы конвертировать используйте такой формат: \n<Название валюты> \
 <В какою валюту перевести> \
 <Количество переводимой валюты>. \nПример: Рубль Доллар 1.\
 \nВвод чувствителен к регистру поэтому будьте внимательны. \
 \
 \nУвидеть список всех доступных валют: \
 \n/values'
    bot.send_message(message.chat.id, text)   


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        options = message.text.split(' ')

        if len(options) != 3:
            raise ConvertionException('Слишком много параметров.')

        #рубль, доллар, 1 
        quote, base, amount = options 
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Переводим {quote} в {base}\n{amount} {quote} = {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()