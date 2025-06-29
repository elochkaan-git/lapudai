from datetime import datetime
from aiogram.utils.keyboard import *


def greetings_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Конечно!"))
    builder.add(KeyboardButton(text="Не уверен..."))
    builder.adjust(2)
    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

def services_kb(index: int, border: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if index == -1:
        builder.add(InlineKeyboardButton(text="Выбрать", callback_data="accept"))
    elif index == 0:
        builder.add(InlineKeyboardButton(text="->", callback_data="+1"))
        builder.add(InlineKeyboardButton(text="Выбрать", callback_data="accept"))
    elif index == border-1:
        builder.add(InlineKeyboardButton(text="<-", callback_data="-1"))
        builder.add(InlineKeyboardButton(text="Выбрать", callback_data="accept"))
    else:
        builder.add(InlineKeyboardButton(text="<-", callback_data="-1"))
        builder.add(InlineKeyboardButton(text="->", callback_data="+1"))
        builder.add(InlineKeyboardButton(text="Выбрать", callback_data="accept"))
    builder.adjust(2)
    return builder.as_markup()

def months_kb() -> ReplyKeyboardMarkup:
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    builder = ReplyKeyboardBuilder()
    for m in months:
        builder.add(KeyboardButton(text=m))
    builder.adjust(2)
    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

def days_kb(month: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    thirty = ['Апрель', 'Июнь', 'Сентябрь', 'Ноябрь']
    thirty_one = ['Январь', 'Март', 'Май', 'Июль', 'Август', 'Октябрь', 'Декабрь']
    
    if month in thirty:
        for i in range(1, 31):
            builder.add(KeyboardButton(text=str(i)))
    elif month in thirty_one:
        for i in range(1, 32):
            builder.add(KeyboardButton(text=str(i)))
    else:
        for i in range(1, 29):
            builder.add(KeyboardButton(text=str(i)))
    builder.adjust(7)

    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=True
    )

def accepting_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Проверить заявки"))
    builder.add(KeyboardButton(text="Остановить процедуру"))
    builder.adjust(1)
    return builder.as_markup(
        resize_keyboard=True
    )

def tasks_kb(index: int, border: int) -> InlineKeyboardMarkup:
    kb = []
    if index == -1:
        kb.append([InlineKeyboardButton(text="Подтвердить", callback_data="apply")])
        kb.append([InlineKeyboardButton(text="Закончить", callback_data="end")])
    elif index == 0:
        kb.append([InlineKeyboardButton(text="->", callback_data="1+")])
        kb.append([InlineKeyboardButton(text="Подтвердить", callback_data="apply")])
        kb.append([InlineKeyboardButton(text="Закончить", callback_data="end")])
    elif index == border-1:
        kb.append([InlineKeyboardButton(text="<-", callback_data="1-")])
        kb.append([InlineKeyboardButton(text="Подтвердить", callback_data="apply")])
        kb.append([InlineKeyboardButton(text="Закончить", callback_data="end")])
    else:
        kb.append(
            [InlineKeyboardButton(text="<-", callback_data="1-"),
            InlineKeyboardButton(text="->", callback_data="1+")]
        )
        kb.append([InlineKeyboardButton(text="Подтвердить", callback_data="apply")])
        kb.append([InlineKeyboardButton(text="Закончить", callback_data="end")])

    return InlineKeyboardMarkup(inline_keyboard=kb)

def stop_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Остановить процедуру")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def back_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='В главное меню')]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def ages_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text='0-6'))
    builder.add(KeyboardButton(text='7-9'))
    builder.add(KeyboardButton(text='10-16'))
    builder.add(KeyboardButton(text='16+'))
    builder.add(KeyboardButton(text='Универсальные мероприятия (для всех возрастов)'))
    builder.adjust(2)
    return builder.as_markup(
        resize_keyboard=True
    )

def yes_or_no_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Да"), KeyboardButton(text="Нет")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

def yes_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Подтверждаю")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )