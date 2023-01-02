from aiogram import executor, Dispatcher, types
from logger import logger
from bot.loader import dp


async def on_startup(dispatcher: Dispatcher):
    await dispatcher.bot.set_my_commands([
        types.BotCommand('start', 'Запустить бота'),
        types.BotCommand('help', 'Помощь'),
        types.BotCommand('show', 'Показать ссылки'),
    ])
    logger.info("Commands added")


async def on_shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    logger.info("Shutdown completed")


if __name__ == "__main__":
    logger.info("Start bot")
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)

