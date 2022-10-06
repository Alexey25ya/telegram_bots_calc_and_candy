import random
import logging
from config import TOKEN
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)
# Включим ведение журнала
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Определяем константы этапов разговора
CANDY_COUNT, PER_TURN , PLAYER_TURN, COMPUTER_TURN = range(4)

# функция обратного вызова точки входа в разговор
def start(update, _):

    update.message.reply_text(
        'Добро пожаловать в игру "Конфеты". Правила игры: На столе лежит 2021 конфета(или сколько вы зададите).'
        'Играют игрок и бот делая ход друг после друга.'
        'За один ход можно забрать не более чем 28 конфет(или сколько вы зададите).' 
        'Тот, кто берет последнюю конфету - проиграл..\n\n'
        'Нажмите q, чтобы выйти из игры или введите количество конфет в куче: ')    
    return CANDY_COUNT


def candy_count(update, context):
    user = update.message.from_user
    logger.info(" %s выбрал количество конфет равное %s", user.first_name, update.message.text)
    candy_count = update.message.text
    if candy_count.isdigit():
        candy_count = int(candy_count)
        context.user_data['candy_count'] = candy_count
        update.message.reply_text(
            f'В куче {candy_count} конфет\n')
        update.message.reply_text(
            f'Введите кол-во конфет, которое можно забрать за ход.\n(Оно должно быть меньше общего колличества конфет в куче): ')  
        return PER_TURN
    elif candy_count =='q':
        return cancel(update, context)
    else:
         update.message.reply_text(
            f'Вы ввели не число\n')



def per_turn(update, context):
    user = update.message.from_user
    logger.info("Пользватель %s выбрал количество конфет  за ход равное  %s", user.first_name, update.message.text)
    candy_count = context.user_data.get('candy_count')
    turn_count = update.message.text
    if turn_count.isdigit():
        turn_count = int(turn_count)
        if candy_count > turn_count and turn_count > 0:
                context.user_data['turn_count'] = turn_count
                update.message.reply_text(
                    f'За ход можно брать от 1 до {turn_count} конфет\n')
                update.message.reply_text(
                f'Ваш ход. Введите число в диапазоне от 1 до {turn_count}: ')
                return PLAYER_TURN
        else:
               update.message.reply_text(f'Максимально допустимое значение {candy_count -1}') 
    else:
         update.message.reply_text(
            f'Вы ввели не число\n')
    


def player_turn(update, context):
    user = update.message.from_user
    logger.info("Ход игрока %s: игрок взял %s конфет ", user.first_name, update.message.text)
    turn_count =context.user_data.get('turn_count')
    candy_count = context.user_data.get('candy_count')
    if candy_count < turn_count:
        turn_count = turn_count - (turn_count - candy_count)
    player_turn = update.message.text
    if player_turn.isdigit():
        player_turn = int(player_turn)
        if player_turn <= turn_count:
                candy_count -= player_turn
                if candy_count < 1:
                    update.message.reply_text(
                        f'Игрок {user.first_name}, вы проиграли\nНажмите /start для новой игры') 
                    return ConversationHandler.END 
                context.user_data['candy_count'] = candy_count
                context.user_data['turn_count']=turn_count
                update.message.reply_text(f'Вы взяли {player_turn} конфет. В куче осталось {candy_count}: ')
                update.message.reply_text(f'Ход переходит боту\n Введите любой символ, чтобы бот сделал ход:')             
                return COMPUTER_TURN
        else:
                update.message.reply_text(
                        f'Максимально возможное количество конфет - {turn_count}')    
    else:
        update.message.reply_text(f'Нужно ввести число')


        
def computer_turn(update, context):
    turn_count = context.user_data.get('turn_count')
    candy_count = context.user_data.get('candy_count')
    if candy_count >= turn_count:
        bot_turn = random.randint(1,turn_count)
        candy_count-=bot_turn
    elif (0 < candy_count <turn_count):
        bot_turn = random.randint(1,candy_count-1)
        candy_count-=bot_turn
    if candy_count <1:
        update.message.reply_text('Бот проиграл\nНажмите /start для новой игры')
        return ConversationHandler.END 
    context.user_data['candy_count'] = candy_count
    context.user_data['turn_count']=turn_count
    update.message.reply_text(f'Бот взял {bot_turn} конфет. В куче осталось {candy_count}: ')
    update.message.reply_text(f'Ваш ход. Введите число в диапазоне от 1 до {turn_count}: ') 
    logger.info(f"Ход игрока бот: бот взял {bot_turn} конфет ")          
    return PLAYER_TURN
    
def cancel(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал о том, что пользователь не разговорчивый
    logger.info("Пользователь %s отменил игру.", user.first_name)
    # Отвечаем на отказ поговорить
    update.message.reply_text(
        'До встречи!'
        'Для запуска игры нажмите /start.' 
    )
    return ConversationHandler.END