
from config import TOKEN
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)
from functions_calc import *

if __name__ == '__main__':
    # Создаем Updater и передаем ему токен вашего бота.
    updater = Updater(TOKEN)
    # получаем диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher


    conversation_handler = ConversationHandler(  # здесь строится логика разговора
        # точка входа в разговор
        entry_points=[CommandHandler('start', start)],
        # этапы разговора, каждый со своим списком обработчиков сообщений
        states={
            CHOICE: [MessageHandler(Filters.text, choice)],
            RATIONAL_ONE: [MessageHandler(Filters.text, rational_one)],
            RATIONAL_TWO: [MessageHandler(Filters.text, rational_two)],
            OPERATIONS_RATIONAL: [MessageHandler(Filters.text, operatons_rational)],
            OPERATIONS_COMPLEX: [MessageHandler(Filters.text, operatons_complex)],
            COMPLEX_ONE: [MessageHandler(Filters.text, complex_one)],
            COMPLEX_TWO: [MessageHandler(Filters.text, complex_two)],
        },
        # точка выхода из разговора
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Добавляем обработчик разговоров `conv_handler`
    dispatcher.add_handler(conversation_handler)

    # Запуск бота
    print('server started')
    updater.start_polling()
    updater.idle()



