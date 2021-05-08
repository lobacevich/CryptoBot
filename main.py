import telebot
from config import TOKEN, keys
from extensions import Converter, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message):
    text = '''Чтобы начать работу, введите команду боту в следующем формате:
<название валюты> <в какую валюту перевести> <количество переводимой валюты>
Увидеть список всех доступных валют: /values'''
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:'
    for key in keys:
        text += '\n' + key
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        value = message.text.split()
        if len(value) != 3:
            raise APIException('Должно быть ровно 3 параметра')
        base, quote, amount = value
        price = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, e)
    except Exception as e:
        bot.reply_to(message, f'Ошибка сервера:\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} будет {price} '
        bot.send_message(message.chat.id, text)


bot.polling()
