from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bd.DBContext import DBContext

import aiogram.utils.markdown as fmt

db = DBContext()


class OrderContributionSelect(StatesGroup):
    waiting_for_contribution_name = State()
    waiting_for_contribution_day = State()
    waiting_for_contribution_where_percent = State()
    waiting_for_contribution_schema = State()
    waiting_for_contribution_percent = State()
    waiting_for_contribution_summa = State()
    waiting_for_contribution_extra_option = State()


async def contribution_name_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in db.get_contribution_name():
        keyboard.add(name)
    await message.answer("Выбирете вклад:", reply_markup=keyboard)
    await OrderContributionSelect.waiting_for_contribution_name.set()


async def get_contrubution_days(message: types.Message, state: FSMContext):
    if message.text.upper() not in db.get_contribution_name():
        await message.answer("Пожалуйста, выбирите один из предложенных вкладов, используя клавиатуру")
        return
    await state.update_data(contribution_name=message.text.upper())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_data = await state.get_data()
    for day in db.get_contribution_day(user_data.get("contribution_name")):
        keyboard.add(str(day))
    await OrderContributionSelect.next()
    await message.answer("Выбирите срок вклада:", reply_markup=keyboard)


async def get_contrubution_where_percent(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if message.text.isdigit() and int(message.text) not in db.get_contribution_day(user_data.get("contribution_name")):
        await message.answer("Пожалуйста, выбирите один из предложенных вариантов, используя клавиатуру")
        return
    await state.update_data(contribution_day=message.text.upper())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_data = await state.get_data()
    for where_percent in db.get_contribution_where_percent(user_data.get("contribution_name")):
        print(where_percent)
        keyboard.add(where_percent)
    await OrderContributionSelect.next()
    await message.answer("Выбирите куда перечислять проценты:", reply_markup=keyboard)


async def get_contrubution_schema(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if message.text.upper() not in db.get_contribution_where_percent(user_data.get("contribution_name")):
        await message.answer("Пожалуйста, выбирите один из предложенных вариантов, используя клавиатуру")
        return
    await state.update_data(contribution_where_percent=message.text.upper())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    user_data = await state.get_data()
    for schema in db.get_contribution_schema_bd(user_data.get("contribution_name"), user_data.get("contribution_day")):
        keyboard.add(schema)
    await OrderContributionSelect.next()
    await message.answer("Выбирите схему начисления процентов:", reply_markup=keyboard)


async def get_contrubution_percent(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if message.text not in db.get_contribution_schema_bd(user_data.get("contribution_name"),
                                                         user_data.get("contribution_day")):
        await message.answer("Пожалуйста, выбирите один из предложенных вариантов, используя клавиатуру")
        return
    await state.update_data(contribution_schema=message.text.upper())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_data = await state.get_data()

    contribution_info = db.get_contribution_percent(user_data.get("contribution_name"),
                                              user_data.get("contribution_day"),
                                              user_data.get("contribution_schema"))

    await state.update_data(contribution_percent=contribution_info[0],
                            contribution_extra_option=contribution_info[1],
                            contribution_min_summa=contribution_info[2])

    user_data = await state.get_data()

    if eval(user_data.get("contribution_extra_option")):
        text_message, dict_extra_options = db.get_contribution_extra_option(user_data.get("contribution_name"))

        for schema in dict_extra_options.keys():
            keyboard.add(schema)
        await OrderContributionSelect.waiting_for_contribution_extra_option.set()
        await message.answer(text_message, reply_markup=keyboard)

    else:
        await OrderContributionSelect.waiting_for_contribution_percent.set()
        await message.answer(f"Для выбранного вклада {user_data.get('contribution_name')} минимальная сумма "
                             f"{format_summ(user_data.get('contribution_min_summa'))} рублей.\n"
                             f"Введите сумму вклада:",
                             reply_markup=types.ReplyKeyboardRemove())


async def get_contribution_extra_option(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    text_message, dict_extra_options = db.get_contribution_extra_option(user_data.get("contribution_name"))

    if message.text not in dict_extra_options.keys():
        await message.answer("Пожалуйста, выбирите один из предложенных вариантов, используя клавиатуру")
        return

    extra_percent = dict_extra_options.get(message.text)
    await state.update_data(contribution_percent=round(float(user_data['contribution_percent'])
                                                       + float(extra_percent), 2))
    user_data = await state.get_data()

    await OrderContributionSelect.waiting_for_contribution_percent.set()
    await message.answer(f"Для выбранного вклада {user_data.get('contribution_name')} минимальная сумма "
                         f"{format_summ(user_data.get('contribution_min_summa'))} рублей.\n"
                         f"Введите сумму вклада:",
                         reply_markup=types.ReplyKeyboardRemove())


async def get_contrubution_summ(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите сумму вклада цифрами.")
        return

    if float(message.text) < float(user_data.get("contribution_min_summa")):
        await message.answer("Вы ввели сумму меньше минимально возможной")
        return

    if float(message.text) > float(db.get_contribution_max_summ()[0]):
        await message.answer("Вы ввели сумму, больше максимально возможной")
        return

    await state.update_data(contribution_summ=message.text)
    user_data = await state.get_data()
    await message.answer(finish_math(user_data), parse_mode='HTML')

    await state.finish()


def finish_math(user_data):
    vklad_name = user_data.get("contribution_name")
    vklad_day = int(user_data.get("contribution_day"))
    vklad_schema = user_data.get("contribution_schema")
    vklad_percent = float(user_data.get("contribution_percent"))
    vklad_summa = float(user_data.get("contribution_summ"))
    vklad_summa_first = float(user_data.get("contribution_summ"))
    vklad_where_percent = user_data.get("contribution_where_percent")

    if vklad_schema == "В КОНЦЕ СРОКА" or vklad_where_percent == "НА ДРУГОЙ СЧЕТ":
        res = []
        summa_d = round((vklad_summa * vklad_percent * vklad_day / 365) / 100, 2)
        res.append(summa_d)

    elif vklad_schema == "ЕЖЕМЕСЯЧНО":
        res = []
        for i in range(0, round(vklad_day / 30)):
            summa_d = round((vklad_summa * vklad_percent * 30 / 365) / 100, 2)
            vklad_summa += summa_d
            res.append(summa_d)

    elif vklad_schema == "ЕЖЕКВАРТАЛЬНО":
        res = []
        for i in range(0, round(vklad_day / 90)):
            summa_d = round((vklad_summa * vklad_percent * 90 / 365) / 100, 2)
            vklad_summa += summa_d
            res.append(summa_d)

    result_txt = fmt.text(fmt.text("Наименование вклада:", fmt.hbold(vklad_name)),
                          fmt.text("Длительность вклада:", fmt.hbold(vklad_day), "дней."),
                          fmt.text("Процент по вкладу:", fmt.hbold(vklad_percent), "%"),
                          fmt.text("Сумма вклада:", fmt.hbold(format_summ(vklad_summa_first)), "руб."),
                          fmt.text("Сумма процентов:", fmt.hbold(format_summ(round(sum(res), 2)), "руб.")),
                          sep="\n"
                          )

    return result_txt


def format_summ(summ):
    return '{0:,}'.format(summ).replace(',', ' ')


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено, начните заново /start", reply_markup=types.ReplyKeyboardRemove())


def register_handlers_contribution(dp: Dispatcher):
    dp.register_message_handler(contribution_name_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(get_contrubution_days,
                                state=OrderContributionSelect.waiting_for_contribution_name)
    dp.register_message_handler(get_contrubution_where_percent,
                                state=OrderContributionSelect.waiting_for_contribution_day)
    dp.register_message_handler(get_contrubution_schema,
                                state=OrderContributionSelect.waiting_for_contribution_where_percent)
    dp.register_message_handler(get_contrubution_percent,
                                state=OrderContributionSelect.waiting_for_contribution_schema)
    dp.register_message_handler(get_contrubution_summ,
                                state=OrderContributionSelect.waiting_for_contribution_percent)
    dp.register_message_handler(get_contribution_extra_option,
                                state=OrderContributionSelect.waiting_for_contribution_extra_option)
