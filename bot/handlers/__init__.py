from aiogram import types
from aiogram.dispatcher import FSMContext

from api import create_link, is_link_exist, get_links
from bot.keyboards import START_KEYBOARD, CANCEL_KEYBOARD, get_links_keyboard
from bot.loader import dp
from bot.states import CreateLink
from bot.utils.misc import is_correct_link, is_correct_source
from logger import logger


@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message):
    state = dp.current_state()
    await state.finish()

    return await message.answer("Hello", reply_markup=START_KEYBOARD)


@dp.message_handler(commands=['show'], state="*")
async def show(message: types.Message):
    state = dp.current_state()
    await state.finish()

    links = await get_links()
    return await message.answer('Выберите ссылку для получения статистики', reply_markup=get_links_keyboard(links))


@dp.callback_query_handler(lambda cb: cb.data.startswith("LINK_"))
async def get_link_info(callback_query: types.CallbackQuery, state: FSMContext):
    print(callback_query.data)
    link_id = int(callback_query.data.split("LINK_")[1])
    return await callback_query.message.answer(f"https://localhost:6575/api/link_info/{link_id}")


@dp.callback_query_handler(lambda cb: cb.data == 'cancel', state="*")
async def cancel(callback_query: types.CallbackQuery, state: FSMContext):
    state = dp.current_state()
    await state.finish()

    await callback_query.message.edit_text("Hello")
    return await callback_query.message.edit_reply_markup(reply_markup=START_KEYBOARD)


@dp.callback_query_handler(lambda cb: cb.data == 'create_link')
async def create_link_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await CreateLink.waiting_redirect_url.set()
    await callback_query.message.edit_text("Введите ссылку, которая будет после https://site.ru/")
    return await callback_query.message.edit_reply_markup(reply_markup=CANCEL_KEYBOARD)


@dp.message_handler(state=CreateLink.waiting_redirect_url)
async def waiting_redirect(message: types.Message, state: FSMContext):
    link = message.text
    logger.debug("Here")
    if not is_correct_link(link):
        return await message.answer("Ссылка содержит недопустимые символы")
    if len(link) > 25:
        return await message.answer("Ссылка слишком длинная (более 25 символов)")
    if await is_link_exist(link):
        return await message.answer("Ссылка уже существует")

    await state.update_data(redirect=link)
    await CreateLink.waiting_source_url.set()
    return await message.answer("Введите исходную ссылку", reply_markup=CANCEL_KEYBOARD)


@dp.message_handler(state=CreateLink.waiting_source_url)
async def waiting_source(message: types.Message, state: FSMContext):
    link = message.text
    if not is_correct_source(link):
        return await message.answer("Неверная ссылка")

    data = await state.get_data()
    redirect = data.get("redirect")
    await state.finish()

    request_data = await create_link(link, redirect)

    await message.answer(f"Ссылка создана. http://{request_data[0]['link']}")
    return await message.answer("Hello", reply_markup=START_KEYBOARD)


