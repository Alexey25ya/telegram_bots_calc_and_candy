import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
  
    ConversationHandler,
)

# Включим ведение журнала
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
# Определяем константы этапов разговора


CHOICE, RATIONAL_ONE, RATIONAL_TWO, OPERATIONS_RATIONAL, OPERATIONS_COMPLEX, COMPLEX_ONE, COMPLEX_TWO = range(7)


 # функция обратного вызова точки входа в разговор
def start(update, _):
    # Список кнопок для ответа
    reply_keyboard = [['Рациональные', 'Комплесные', 'Выход']]
    # Создаем простую клавиатуру для ответа
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    # Начинаем разговор с вопроса
    update.message.reply_text(
        'Приветствую Вас в калькуляторе. \n'
        'Нажмите КНОПКУ внизу: \n'
        '  -Операций с рациональными числами \n  -Операции с комплесными числами\n  -Выход \n',
        reply_markup=markup_key,)
    # переходим к этапу `GENDER`, это значит, что ответ
    # отправленного сообщения в виде кнопок будет список 
    # обработчиков, определенных в виде значения ключа `GENDER`
    return CHOICE

def choice(update, context):
    user = update.message.from_user
    logger.info("Пользователь %s ввел %s", user.first_name, update.message.text)
    user_choice = update.message.text
    if user_choice == 'Рациональные':
        update.message.reply_text(
            'Введите первое рациональное число (дробную часть через ".")',reply_markup=ReplyKeyboardRemove())
        return RATIONAL_ONE
    if user_choice == 'Комплесные':
        context.bot.send_message(
            update.effective_chat.id, 'Введите вещественную и мнимую части первого числа через пробел: ',reply_markup=ReplyKeyboardRemove())
        return COMPLEX_ONE
    if user_choice == 'Выход':
        return cancel(update, context)


def rational_one(update, context):
    user = update.message.from_user
    logger.info("Пользователь %s ввел %s", user.first_name, update.message.text)
    get_rational = update.message.text
    if get_rational==str(float(get_rational)):
        get_rational = float(get_rational)
        context.user_data['rational_one'] = get_rational
        update.message.reply_text(
            'Введите второе рациональное число (дробную часть через ".")')
        return RATIONAL_TWO
    else:
        update.message.reply_text(
            'Нужно ввести число')


def rational_two(update, context):
    user = update.message.from_user
    logger.info("Пользователь %s ввел %s", user.first_name, update.message.text)
    get_rational = update.message.text
    if get_rational == str(float(get_rational)):
        get_rational = float(get_rational)
        context.user_data['rational_two'] = get_rational
        update.message.reply_text(
            'Введите в сообщении желаемую операцию над числами: \n\n+ -сложение \n- - разность \n* - умножение \n** - возведение в степень  \n/ - деление \n')
        return OPERATIONS_RATIONAL


def operatons_rational(update, context):
    user = update.message.from_user
    logger.info("Пользователь %s ввел %s", user.first_name, update.message.text)
    rational_one = context.user_data.get('rational_one')
    rational_two = context.user_data.get('rational_two')
    user_choice = update.message.text
    if user_choice == '+':
        result = rational_one + rational_two
    if user_choice == '-':
        result = rational_one - rational_two
    if user_choice == '*':
        result = rational_one * rational_two
    if user_choice == '**':
        result = rational_one ** rational_two
    if user_choice == '/':
        try:
            result = rational_one / rational_two
        except:
            update.message.reply_text('Деление на ноль запрещено')
    update.message.reply_text(
        f'Результат: {rational_one} {user_choice} {rational_two} = {result}\n Для вызова калькулятора жми /start')
    return ConversationHandler.END


def complex_one(update, context):
    user = update.message.from_user
    logger.info("Пользователь %s ввел %s", user.first_name, update.message.text)
    user_choice = update.message.text
    user_choice = user_choice.split(' ')
    complex_one = complex(int(user_choice[0]), int(user_choice[1]))
    context.user_data['complex_one'] = complex_one
    update.message.reply_text(
        f'Первое число {complex_one},  Введите вещественную и мнимую части второго числа через пробел: ')
    return COMPLEX_TWO


def complex_two(update, context):
    user = update.message.from_user
    logger.info("Пользователь %s ввел %s", user.first_name, update.message.text)
    user_choice = update.message.text
    user_choice = user_choice.split(' ')
    complex_two = complex(int(user_choice[0]), int(user_choice[1]))
    context.user_data['complex_two'] = complex_two
    update.message.reply_text(
        f'Второе число {complex_two}, Введите в сообщении желаемую операцию над числами: \n\n+ -сложение \n- - разность \n* - умножение \n** - возведение в степень  \n/ - деление \n')
    return OPERATIONS_COMPLEX


def operatons_complex(update, context):
    user = update.message.from_user
    logger.info("Пользователь %s ввел %s", user.first_name, update.message.text)
    complex_one = context.user_data.get('complex_one')
    complex_two = context.user_data.get('complex_two')
    user_choice = update.message.text
    if user_choice == '+':
        result = complex_one + complex_two
    if user_choice == '-':
        result = complex_one - complex_two
    if user_choice == '*':
        result = complex_one * complex_two
    if user_choice == '**':
        result = complex_one ** complex_two
    if user_choice == '/':
        try:
            result = complex_one / complex_two
        except:
            update.message.reply_text('Деление на ноль запрещено')
    update.message.reply_text(
        f'Результат: {complex_one} {user_choice} {complex_two} = {result}\n Для вызова калькулятора жми /start')
    return ConversationHandler.END


# Обрабатываем команду /cancel если пользователь отменил разговор
def cancel(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал о том, что пользователь не разговорчивый
    logger.info("Пользователь %s отменил разговор.", user.first_name)
    # Отвечаем на отказ поговорить
    update.message.reply_text(
        'Всего доброго!\n'
        'Для вызова калькулятора жми /start', 
        reply_markup=ReplyKeyboardRemove()
    )
    # Заканчиваем разговор.
    return ConversationHandler.END
