from aiogram import types, Dispatcher
from keyboards import menu_markup, today_tomorrow_markup, timetable_markup, timetable_someone_markup
from scripts import *
from handlers.fsm import FSM_timetable, FSM_start
from scripts.sql import get_profile
from scripts.excel import get_group_by_fio, get_course_by_fio, is_a_group, is_a_student_by_fi


async def timetable(message: types.Message):
    if message.text == 'Расписание на неделю':
        text = get_week_timetable(str(message.from_user))
        await message.answer(text)
    if message.text == 'Расписание на день':
        await message.answer('Выбери нужный день', reply_markup=today_tomorrow_markup())
        await FSM_timetable.today_tomorrow.set()
    if message.text == 'Какая у меня сейчас пара':
        fio = get_profile(message.from_user.id)
        group = get_group_by_fio(fio)
        text = get_now_lesson(group)
        await message.answer(text)
    if message.text == 'Узнать пары у другого человека':
        await message.answer('Введи номер группы или фамилию с именем', reply_markup=timetable_someone_markup())
        await FSM_timetable.someone_timetable.set()

    if message.text == 'Назад в меню':
        fio = get_profile(message.from_user.id)
        course = get_course_by_fio(fio)
        group = get_group_by_fio(fio)
        await message.answer(
            f'Привет, {fio}, я готов тебе помогать\n\nФИО: {fio} \nКурс: {course} \nГруппа: {group} \nЧто тебе нужно?',
            reply_markup=menu_markup())
        await FSM_start.menu.set()


async def timetable_day_lessons(message: types.Message):
    if message.text == 'Пары сегодня':
        fio = get_profile(message.from_user.id)
        group = get_group_by_fio(fio)
        text = get_today_lessons(group)
        await message.answer(text)
    if message.text == 'Пары завтра':
        fio = get_profile(message.from_user.id)
        group = get_group_by_fio(fio)
        text = get_tomorrow_lessons(group)
        await message.answer(text)
    if message.text == 'Вернуться в расписание':
        await message.answer('Выбери расписание', reply_markup=timetable_markup())
        await FSM_timetable.timetable.set()


async def timetable_someone(message: types.Message):
    if is_a_student_by_fi(message.text) or is_a_group(message.text):
        if is_a_student_by_fi(message.text):
            group = get_group_by_fi(message.text)
        else:
            group = message.text
        text = get_today_lessons(group)
        await message.answer(text, reply_markup=timetable_markup())
        await FSM_timetable.timetable.set()
    elif message.text == 'Вернуться в расписание':
        await message.answer('Выбери расписание', reply_markup=timetable_markup())
        await FSM_timetable.timetable.set()

    else:
        await message.answer('Такого ученика/группы нету, попробуйте ввести заново')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(timetable, state=FSM_timetable.timetable)
    dp.register_message_handler(timetable_day_lessons, state=FSM_timetable.today_tomorrow)
    dp.register_message_handler(timetable_someone, state=FSM_timetable.someone_timetable)