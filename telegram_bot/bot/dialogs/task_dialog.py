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
    categories_for_select = [
      (cat.get('name', 'Unknown'), str(cat.get('id')))
        for cat in categories if cat is not None
    ]
    print(categories, categories_for_select)
    return {'categories': categories_for_select}


async def on_category_selected(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['category_id'] = item_id
    await dialog_manager.next()

category_window = Window(
    Const('➡️ Step 3/5. Select a category:'),
    Select(id='s_category',
    item_id_getter=operator.itemgetter(1),
    items='categories',
    on_click=on_category_selected,
           text=Format('🔘 {item[0]}')
           ),
    getter=category_getter,
    state=TaskCreation.category


)


async def on_date_selected(callback: CallbackQuery, widget: Calendar, dialog_manager: DialogManager, selected_date: date):
    dialog_manager.dialog_data['due_date'] = selected_date.isoformat()
    await callback.answer()
    await dialog_manager.next()

date_window = Window(
    Const('➡️ Step 4/5. Select a due date:'),
    Calendar(
        id='c_date',
        on_click=on_date_selected
    ),
    state=TaskCreation.due_date
)


async def confirm_getter(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.dialog_data
    category_id = data.get('category_id')
    all_categories = data.get('all_categories', [])
    category_name = next(
       (cat.get('name') for cat in all_categories if category_id == str(cat.get('id'))),
        'Category not found'
    )

    return {
        'title': data.get('title', '-'),
        'description': data.get('description', '-'),
        'category': category_name,
        'due_date': data.get('due_date', 'Date not selected')
    }

async def on_confirm(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    task_data = {
        'username': callback.from_user.username,
        'telegram_id': callback.from_user.id,
        'title': dialog_manager.dialog_data.get('title'),
        'description': dialog_manager.dialog_data.get('description'),
        'category': dialog_manager.dialog_data.get('category_id'),
        'due_date': dialog_manager.dialog_data.get('due_date'),
    }
    try:
        task_create = await API_CLIENT.create_task(**task_data)
        if task_create:
            await callback.message.answer('Task create successfully! 🎉')
        else:
            await callback.message.answer('Creation error. Try again! ❌')
    except Exception as e:
        await callback.message.answer('Creation error. Try again! ❌')

    await dialog_manager.done()

confirm_window = Window(
    Const('➡️ Step 5/5. Please confirm the task details:'),
    Format('<b>Title:</b> {title}'),
    Format("<b>Description:</b> {description}"),
    Format("<b>Category:</b> {category}"),
    Format("<b>Due Date:</b> {due_date}"),
    Button(Const('✅ Save Task'), id='confirm_btn', on_click=on_confirm),
    Cancel(Const('❌ Cancel'), ),
    state=TaskCreation.confirm,
    getter=confirm_getter
)


task_dialog = Dialog(title_window, description_window, category_window, date_window, confirm_window)


