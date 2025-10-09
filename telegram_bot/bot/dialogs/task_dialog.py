import operator
from datetime import date

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Cancel, Select, Calendar
from aiogram_dialog.widgets.input import TextInput

from .states import TaskCreation
from telegram_bot.bot.api_client import DjangoAPIClient
from telegram_bot.bot.config import API_CLIENT


async def title_input(message: Message, widget: TextInput, dialog_manager: DialogManager, title_text: str):
    dialog_manager.dialog_data['title'] = title_text
    await dialog_manager.next()

title_window = Window(
    Const('➡️ Step 1/5. Enter the task name:'),
    TextInput(
        id='title_input',
        on_success=title_input
    ),
    state=TaskCreation.title
)

async def description_input(message: Message, widget: TextInput, dialog_manager: DialogManager, description_text: str):
    dialog_manager.dialog_data['description'] = description_text
    await dialog_manager.next()

description_window = Window(
    Const('➡️ Step 2/5. Enter the task description:'),
    TextInput(
        id='description_input',
        on_success=description_input
    ),
    state=TaskCreation.description
)

async def category_getter(dialog_manager: DialogManager, **kwargs):
    categories = await API_CLIENT.get_categories()
    dialog_manager.dialog_data['all_categories'] = categories
    return {'categories': categories}

task_dialog = Dialog(title_window, description_window)


