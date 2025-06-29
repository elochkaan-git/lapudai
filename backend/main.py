import os, sys
sys.path.append("../config")

import asyncio
from datetime import datetime
import logging
import sqlite3
import re

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, FSInputFile, InputMediaPhoto, ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.state import any_state

from db import pgManager
from keyboards import *
from classes import ChooseService, AdminsActions
from gcalendar import add_event
from tokenBot import TOKEN

from sqlitestorage.storage import SQLiteStorage


bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dispatcher = Dispatcher(storage=SQLiteStorage(db_path="./backend/users.db"))
logging.basicConfig(level=logging.INFO)
pgmgr = pgManager('lapudai', 'manager', '1234567890', 'db')
admins = open('./config/admins.txt', 'r').readlines()


""" -ОБЩИЕ ФУНКЦИИ- """

# Стоят несколько фильтров:
# 1. Если была набрана команда /start
# 2. Если была нажата кнопка "В главное меню"
@dispatcher.message(
    Command("start"),
    StateFilter(any_state),
    ~StateFilter(ChooseService.waiting)
)
@dispatcher.message(
    F.text == 'В главное меню',
    StateFilter(any_state),
    ~StateFilter(ChooseService.waiting)
)
async def greetings(message: Message, state: FSMContext):
    """Функция приветствия. Определяет, является ли пользователем менеджером
    и действует в соответствии с ответом
    """

    if str(message.from_user.id) not in admins:
        await state.clear()
        if await pgmgr.is_user_exist(message.from_user.id):
            await message.answer(
                text="Здравствуйте! Вас приветствует компания Лапудай. Вы уже знаете, что хотите выбрать?",
                reply_markup=greetings_kb()
            )
        else:
            await message.answer(
                text="Здравствуйте! Вас приветствует компания Лапудай. Пожалуйста, для начала отправьте ваш номер телефона.",
                reply_markup=ReplyKeyboardRemove()
            )
            await state.set_state(ChooseService.number)

        data = await state.get_data()
        data['age'] = ''
        data['index'] = 0
        data['month'] = ''
        data['day'] = ''
        data['date'] = ''
        data['guests'] = ''
        data['service'] = ''
        data['admin_id'] = ''
        data['number'] = ''
        data['name'] = ''

        await state.set_data(data)
    else:
        data = await state.get_data()
        data['client_id'] = ''
        data['task_id'] = ''
        data['index'] = 0
        data['date'] = ''
        data['start'] = ''
        data['end'] = ''
        await message.answer(
            text="Готовы проверять заявки? :)",
            reply_markup=accepting_kb()
        )
        await state.clear()
        await state.set_data(data)
        await state.set_state(AdminsActions.accepting)

""" -ФУНКЦИИ ДЛЯ АДМИНИСТРАЦИИ- """

@dispatcher.message(
    AdminsActions.accepting,
    F.text == 'Проверить заявки'
)
async def choose_services(message: Message, state: FSMContext):
    data = await state.get_data()
    tasks = await pgmgr.get_all_tasks()

    try:
        if len(tasks) == 0:
            await message.answer(
                text='Пока что заявок нет',
                reply_markup=back_kb(),
                parse_mode='HTML'
            )
        if len(tasks) == 1:
            await message.answer(
                text=str(tasks[0].format()),
                reply_markup=tasks_kb(-1, len(tasks)),
                parse_mode="HTML"
            )
        else:
            await message.answer(
                text=str(tasks[0].format()),
                reply_markup=tasks_kb(0, len(tasks)),
                parse_mode="HTML"
            )
        data['task_id'] = tasks[data['index']].id
        data['client_id'] = tasks[data['index']].cliend_id

    except IndexError as e:
        logging.warning("There's no tasks available")

    await state.set_data(data)


@dispatcher.callback_query(
    AdminsActions.accepting,
    F.data.in_(['1+', '1-']) 
)
async def view_tasks(callback: CallbackQuery, state: FSMContext):
    tasks = await pgmgr.get_all_tasks()
    data = await state.get_data()

    if callback.data == '1-':
        data['index'] -= 1
    elif callback.data == '1+':
        data['index'] += 1
    data['client_id'] = tasks[data['index']].cliend_id
    data['task_id'] = tasks[data['index']].id
    if len(tasks) == 1:
        await callback.message.edit_text(
            text=tasks[data['index']].format(),
            reply_markup=tasks_kb(-1, len(tasks)),
            parse_mode="HTML"
        )
    else:
        await callback.message.edit_text(
            text=tasks[data['index']].format(),
            reply_markup=tasks_kb(data['index'], len(tasks)),
            parse_mode="HTML"
        )

    await state.set_data(data)


@dispatcher.callback_query(
    F.data == 'apply'
)
async def apply(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await pgmgr.add_chat(callback.message.chat.id, int(data['client_id']))

    await callback.message.answer(
        text="Вы связались с клиентом. Приятного общения!",
        reply_markup=stop_kb()
    )
    await bot.send_message(
        chat_id=data['client_id'],
        text=f"С вами связался менеджер. Приятного общения!",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(AdminsActions.apply)


@dispatcher.message(
    AdminsActions.apply, 
    F.text != 'Остановить процедуру'
)
async def ask_date(message: Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(
        chat_id=data['client_id'],
        text=message.text,
        reply_markup=ReplyKeyboardRemove()
    )


@dispatcher.message(
    AdminsActions.apply,
    F.text == "Остановить процедуру", 
)
async def final(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(
        text="Поздравляю, клиент записан! Чат с клиентом закрыт",
        reply_markup=accepting_kb()
    )
    await bot.send_message(
        chat_id=data['client_id'],
        text="Поздравляю, вы записаны! Чат с менеджером окончен.",
        reply_markup=back_kb()
    )
    
    new_user_storage_key = StorageKey(bot.id, int(data['client_id']), int(data['client_id']))
    new_user_context = FSMContext(storage=dispatcher.storage, key=new_user_storage_key)
    await new_user_context.update_data({
        'age' : '',
        'index' : 0,
        'month' : '',
        'day' : '',
        'date' : '',
        'guests' : '',
        'service' : '',
        'admin_id' : ''
    })
    await new_user_context.set_state(ChooseService.back)

    await pgmgr.delete_task(int(data['task_id']))
    await pgmgr.delete_chat(int(data['client_id']))
    data['client_id'] = ''
    data['task_id'] = ''
    data['index'] = 0
    data['date'] = ''
    data['start'] = ''
    data['end'] = ''
    await state.set_data(data)
    await state.set_state(AdminsActions.accepting)


@dispatcher.callback_query(
    F.data == 'end'
)
async def end(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data['client_id'] = ''
    data['task_id'] = ''
    data['index'] = 0
    data['date'] = ''
    data['start'] = ''
    data['end'] = ''
    
    await callback.message.answer(
        text="На сегодня хватит работы В)"
    )
    await state.clear()
    await state.set_data(data)


@dispatcher.message(
    F.text == "Остановить процедуру"
)
async def end(message: Message, state: FSMContext):
    data = await state.get_data()
    data['client_id'] = ''
    data['task_id'] = ''
    data['index'] = 0
    data['date'] = ''
    data['start'] = ''
    data['end'] = ''

    await message.answer(
        text="На сегодня хватит работы В)"
    )
    await state.set_data(data)
    await state.set_state(AdminsActions.accepting)


""" -ФУНКЦИИ ДЛЯ КЛИЕНТОВ- """

@dispatcher.message(
    F.content_type == ContentType.TEXT,
    ChooseService.number
)
@dispatcher.message(
    F.content_type == ContentType.CONTACT,
    ChooseService.number
)
async def user_number(message: Message, state: FSMContext):
    try:
        phone_number = message.contact.phone_number[1::]
    except:
        logging.warning('Пользователь отправил не контакт, а текст')
        phone_number = re.sub(r'\D', '', message.text)

    await state.update_data(number=phone_number)
    await message.answer(
        text="Отлично! Теперь, пожалуйста, введите ваше имя.",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(ChooseService.name)


@dispatcher.message(
    ChooseService.name
)
async def user_name(message: Message, state: FSMContext):
    data = await state.get_data()
    await pgmgr.add_user(message.from_user.id, data['number'], message.text)
    await message.answer(
        text="Спасибо за регистрацию! Теперь вы можете вернуться к выбору услуг.",
        reply_markup=back_kb()
    )
    await state.set_data(data)


@dispatcher.message(
    F.text == 'Конечно!'
)
async def choose_services(message: Message, state: FSMContext):
    services = await pgmgr.get_services()
    photo = FSInputFile(services[0].imgpath)
    if len(services) == 1:
        await message.answer_photo(
            photo=photo,
            caption=services[0].format(),
            reply_markup=services_kb(-1, len(services)),
            parse_mode="HTML"
        )
    else:
        await message.answer_photo(
            photo=photo,
            caption=services[0].format(),
            reply_markup=services_kb(0, len(services)),
            parse_mode="HTML"
        )


@dispatcher.message(
    F.text == 'Не уверен...'
)
async def choose_age(message: Message, state: FSMContext):
    await message.answer(
        text='Выберите основной возраст гостей',
        reply_markup=ages_kb(),
    )
    await state.update_data(index=0)
    await state.set_state(ChooseService.ages)


@dispatcher.message(
    ChooseService.ages
)
async def choose_services_via_age(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == '0-6':
        services = await pgmgr.get_services(category="baby")
        data['age'] = 'baby'
    elif message.text == '7-9':
        services = await pgmgr.get_services(category="bbaby")
        data['age'] = 'bbaby'
    elif message.text == '10-16':
        services = await pgmgr.get_services(category="teen")
        data['age'] = 'teen'
    elif message.text == '16+':
        services = await pgmgr.get_services(category="old")
        data['age'] = 'old'
    elif message.text == 'Универсальные мероприятия (для всех возрастов)':
        services = await pgmgr.get_services(category="uni")
        data['age'] = 'uni'
    
    try:
        photo = FSInputFile(services[0].imgpath)
        await message.answer_photo(
            photo=photo,
            caption=services[0].format(),
            reply_markup=services_kb(0, len(services)),
            parse_mode='HTML',
        )
    except IndexError:
        logging.warning(f'Внимание! Нет услуг в возрастной категории {data["age"]}')
        await message.answer(
            text='В настоящий момент для данной возрастной категории не предусмотрены услуги.',
            reply_markup=ages_kb()
        )

    data['index'] = 0
    await state.set_data(data)


@dispatcher.callback_query(
    F.data.in_(['+1', '-1'])
)
async def list_of_services(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['age'] == 'baby':
        services = await pgmgr.get_services(category="baby")
    elif data['age'] == 'bbaby':
        services = await pgmgr.get_services(category="bbaby")
    elif data['age'] == 'teen':
        services = await pgmgr.get_services(category="teen")
    elif data['age'] == 'old':
        services = await pgmgr.get_services(category="old")
    elif data['age'] == 'uni':
        services = await pgmgr.get_services(category="uni")
    else:
        services = await pgmgr.get_services()

    if callback.data == '-1':
        data['index'] -= 1
    elif callback.data == '+1':
        data['index'] += 1
    photo = InputMediaPhoto(
        media=FSInputFile(services[data['index']].imgpath), 
        caption=services[data['index']].format(),
        parse_mode="HTML"
    )
    
    await callback.message.edit_media(
        media=photo,
        reply_markup=services_kb(data['index'], len(services)),
    )

    await state.set_data(data)


@dispatcher.callback_query(
    F.data == "accept"
)
async def choose_month(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data['service'] += (callback.message.caption.split('\n')[0] + '///')

    await callback.message.answer(
        text="Выберите месяц, на который хотите записаться.",
        reply_markup=months_kb()
    )
    await state.set_data(data)
    await state.set_state(ChooseService.month)


@dispatcher.message(
    F.text.in_(['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']),
    ChooseService.month
)
async def choose_day(message: Message, state: FSMContext):
    months = {
        'Январь' : '01',
        'Февраль' : '02',
        'Март' : '03',
        'Апрель' : '04',
        'Май' : '05',
        'Июнь' : '06',
        'Июль' : '07',
        'Август' : '08',
        'Сентябрь' : '09',
        'Октябрь' : '10',
        'Ноябрь' : '11',
        'Декабрь' : '12'
    }
    
    data = await state.get_data()
    data['month'] += (months[message.text] + '///')
    
    await message.answer(
        text="Выберите день.",
        reply_markup=days_kb(message.text)
    )
    await state.set_data(data)
    await state.set_state(ChooseService.day)


@dispatcher.message(
    F.text.regexp(r"\d+"),
    ChooseService.day
)
async def number_of_guests(message: Message, state: FSMContext):
    data = await state.get_data()
    if int(message.text) < 10:
        data['day'] += '0' + message.text + '///'
    else:
        data['day'] += message.text + '///'

    data['date'] = ''
    for date in zip(data['month'].split('///')[:-1], data['day'].split('///')[:-1]):
        if date[0] + date[1] < datetime.now().strftime("%m%d"):
            data['date'] += ('.'.join([date[1], date[0], str(datetime.now().year+1)]) + '///')
        else:
            data['date'] += ('.'.join([date[1], date[0], str(datetime.now().year)]) + '///')
    logging.warning(data['date'])

    await message.answer(
        text="Сколько гостей планирует прийти?",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_data(data)
    await state.set_state(ChooseService.guests)


@dispatcher.message(
    ChooseService.guests
)
async def user_number(message: Message, state: FSMContext):
    data = await state.get_data()
    data['guests'] += (message.text + '///')
    await message.answer(
        text="Хотите выбрать еще услуги?",
        reply_markup=yes_or_no_kb()
    )
    await state.set_data(data)
    await state.set_state(ChooseService.more)


@dispatcher.message(
    ChooseService.more,
    F.text.in_(["Да", "Нет"])
)
async def more(message: Message, state: FSMContext):
    logging.warning(message.text)
    if message.text == "Да":
        await choose_services(message, state)
    elif message.text == "Нет":
        await final(message, state)


async def final(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(
        text="Вы оставили заявку. Скоро с вами свяжется наш менеджер для уточнения деталей. Спасибо, что выбираете нас :)",
        reply_markup=ReplyKeyboardRemove()
    )
    
    user = await pgmgr.get_user(message.from_user.id)
    task_id = await pgmgr.create_task(user.id, user.phone, user.name, data['service'], data['guests'], data['date'])
    task = await pgmgr.get_task(task_id)
    for service_id, date in enumerate(data['date'].split('///')[:-1], 0):
        add_event(task, day=date, service_id=service_id)
    await state.set_state(ChooseService.waiting)


@dispatcher.message(
    ChooseService.waiting
)
async def dialog(message: Message, state: FSMContext):
    chat = await pgmgr.get_chat(message.from_user.id)
    logging.warning(chat)
    if chat != []:
        await bot.send_message(
            chat_id=chat['adresat'],
            text=message.text
        )


async def main():
    try:
        await pgmgr.connect()
        await bot.delete_webhook(drop_pending_updates=True)
        await dispatcher.start_polling(bot)
    finally:
        await pgmgr.close()


if __name__ == '__main__':
    asyncio.run(main())
