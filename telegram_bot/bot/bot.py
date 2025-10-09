import asyncio
from aiogram import F
from aiogram.types import Message
from aiogram_dialog import setup_dialogs, DialogManager, StartMode

from .config import bot, dp
import logging

from .dialogs.task_dialog import task_dialog
from .dialogs.states import TaskCreation

@dp.message(F.text == '/start')
async def handle_start(message: Message):
    await message.answer(f'Hello, <b>{message.from_user.username}</b>! I am a bot to manage tasks.'
                         f' To start a dialogue to create a task, use the command /new_task.')

@dp.message(F.text == '/new_task')
async def cmd_mew_task(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        TaskCreation.title,
        mode=StartMode.RESET_STACK
    )





async def main():
    dp.include_router(task_dialog)
    setup_dialogs(dp)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
        logging.info('Bot running')
    except (KeyboardInterrupt, SystemExit):
        logging.error('Bot stopped')
