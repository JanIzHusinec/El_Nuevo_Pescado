import telebot
import time

# Создаем объект бота и токен
bot = telebot.TeleBot('7001950581:AAH5SGxa8IPFD0HOpevsmiz652NgN8fYUy4')

# Словарь для хранения статистики чата
stats = {}

# Обработчик команды /start

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Доброго времени суток, камрад! Имей в виду: Я - бот для управления чатом, а не какой-нибудь малолетний дебил. Напиши /help, чтобы узнать, что как я прекрасен.")

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "/kick - невиннорастрелять пользователя\n/mute - невиннорепрессировать на время\n/unmute - амнистировать пользователя\n/stats - показать досье на камрадов\n/selfstat - показать досье на самого себя")

# Обработчик команды /kick
@bot.message_handler(commands=['kick'])
def kick_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "В ЦК не дураки сидят.")
        else:
            bot.kick_chat_member(chat_id, user_id)
            bot.reply_to(message, f"Камрад {message.reply_to_message.from_user.username} был расстрелян.")
    else:
        bot.reply_to(message, "Этот донос должен быть использован в ответ на сообщение камрада, который вам не пришелся по вкусу.")

# Обработчик команды /mute
@bot.message_handler(commands=['mute'])
def mute_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно заглушить грозный голос Наркома партии.")
        else:
            duration = 60 # Значение по умолчанию - 1 минута
            args = message.text.split()[1:]
            if args:
                try:
                    duration = int(args[0])
                except ValueError:
                    bot.reply_to(message, "У нас столько не сидят.")
                    return
                if duration < 1:
                    bot.reply_to(message, "Это он получается ещё не отсидел, а уже вышел - чудеса да и только, малолетний ты дебил!")
                    return
                if duration > 1440:
                    bot.reply_to(message, "Больше чем на пятнадцать суток задерживать не имею права.")
                    return
            bot.restrict_chat_member(chat_id, user_id, until_date=time.time()+duration*60)
            bot.reply_to(message, f"Камрад {message.reply_to_message.from_user.username} сослан в Серпантинку на {duration} лет.")
    else:
        bot.reply_to(message, "Этот донос должен быть использован в ответ на сообщение камрада, потерявшего общественное доверие. Пусть его настигнет суровая кара нашего закона, всеобщая ненависть и презрение! Но ненадолго.")

# Обработчик команды /unmute
@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        bot.restrict_chat_member(chat_id, user_id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True, can_add_web_page_previews=True)
        bot.reply_to(message, f"Камрад {message.reply_to_message.from_user.username}  был амнистирован указом Президиума Верховного Совета КПВЕКК от сего числа.")
    else:
        bot.reply_to(message, "Эта донос должен быть использован в ответ на сообщение камрада, вновь приобретшего общественное доверие.")

# Обработчик команды /stats
@bot.message_handler(commands=['stats'])
def chat_stats(message):
    chat_id = message.chat.id
    if chat_id not in stats:
        bot.reply_to(message, "Досье данной ОПГ пока пусто.")
    else:
        total_messages = stats[chat_id]['total_messages']
        unique_users = len(stats[chat_id]['users'])
        bot.reply_to(message, f"Досье на ОПГ:\nВсего сообщений: {total_messages}\Камрадов с oper.ru: {unique_users}")

# Обработчик команды /selfstat
@bot.message_handler(commands=['selfstat'])
def user_stats(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    if chat_id not in stats:
        bot.reply_to(message, "Досье данной ОПГ пока пусто.")
    else:
        if user_id not in stats[chat_id]['users']:
            bot.reply_to(message, "Вы еще не успели опозориться.")
        else:
            user_messages = stats[chat_id]['users'][user_id]['messages']
            total_messages = stats[chat_id]['total_messages']
            percentage = round(user_messages / total_messages * 100, 2)
            bot.reply_to(message, f"Досье для пользователя @{username}:\nВсего сообщений: {user_messages}\nПроцент от общего количества сообщений: {percentage}%")

greeting_words = ['Привет', 'Шалом', 'Здарова']

bad_words = ['подработка', 'халтурка', 'темка']

# функция для проверки наличия запрещенных слов в сообщении
def check_message(message):
    for word in bad_words:
        if word in message.text.lower():
            return True
    return False

# функция для проверки наличия запрещенных слов в сообщении
def check_mansarda(message):
    for word in greeting_words:
        if word in message.text.lower():
            return True
    return False


# обработчик сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # проверяем сообщение на наличие запрещенных слов
    if check_message(message):
        # если есть хотя бы одно запрещенное слово, кикаем пользователя
        bot.kick_chat_member(message.chat.id, message.from_user.id)
        bot.send_message(message.chat.id, f"Камрад {message.from_user.username} был избит и с позором загнан под шконку за гнилой базар.")
        # если запрещенных слов нет, обрабатываем сообщение дальше
    if check_mansarda(message):
        # если есть хотя бы одно приветственное слово, приветствуем пользователя
        bot.send_message(message.chat.id, f"Здравствуй, {message.from_user.username}, присаживайся поудобнее. Дементий опять уснул, поэтому чай и свиньи будут потом.")
    else:
        # если приветственных слов нет, обрабатываем сообщение дальше
        
        
        
        print(message.text)






# Запускаем бота
bot.infinity_polling(none_stop=True)
