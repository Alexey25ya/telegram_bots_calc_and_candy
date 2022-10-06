
from config import TOKEN
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)
from functions_candy import *

if __name__ == '__main__':
    # Создаем Updater и передаем ему токен вашего бота.
    updater = Updater(TOKEN)
    # получаем диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher


    game_conversation_handler = ConversationHandler( # здесь строится логика разговора
        # точка входа в разговор
        entry_points=[CommandHandler('start', start)],
        # этапы разговора, каждый со своим списком обработчиков сообщений
        states={
            CANDY_COUNT:[MessageHandler(Filters.text, candy_count),CommandHandler('cancel', cancel)],
            PER_TURN: [MessageHandler(Filters.text, per_turn)],
            PLAYER_TURN:[MessageHandler(Filters.text, player_turn)],
            COMPUTER_TURN: [MessageHandler(Filters.text, computer_turn)],
        },
        # точка выхода из разговора
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Добавляем обработчик разговоров `conv_handler`
    dispatcher.add_handler(game_conversation_handler)

    # Запуск бота
    updater.start_polling()
    updater.idle()



