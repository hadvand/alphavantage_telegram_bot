from aiogram import Bot, Dispatcher, types
from settings import SiteSettings
from site_api.core import headers, site_api, url
from .utils.states import GetArg
from database.common.models import db, History
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage


site = SiteSettings()

bot = Bot(token=site.api_token.get_secret_value())
dp = Dispatcher(bot=bot, storage=MemoryStorage)


@dp.message(commands=['start'])
async def send_hello(message: types.Message):
    await message.reply("Hi!")


@dp.message(commands=['quote'])
async def quote_get_arg(message: types.Message, state: FSMContext):
    await state.set_state(GetArg.quote_arg)
    await message.answer('Enter the name of the ticker you are interested in')


@dp.message(state=GetArg.quote_arg)
async def quote_endpoint(message: types.Message, state: FSMContext):
    await state.update_data(quote_arg=message.text)
    await state.clear()
    ticker_name = message.text
    quote = site_api.getter()
    response = quote(method="GET",
                     url=url,
                     headers=headers,
                     querystring={"symbol": ticker_name, "function": 'GLOBAL_QUOTE'})

    if isinstance(response, int):
        await message.answer('Error', str(response))
        exit(1)

    response = response.json()['Global Quote']
    answer = ''

    for key, value in response.items():
        answer += f'{key[4:]}: {value}\n'

    await message.answer(answer)


@dp.message(commands=['all'])
async def all_endpoint(message: types.Message):
    get_all = site_api.getter()
    response = get_all(method="GET",
                       url=url,
                       headers=headers,
                       querystring={"function": 'LISTING_STATUS'})

    if isinstance(response, int):
        await message.answer('Error', str(response))
        exit(1)

    await message.answer(response)


@dp.message(commands=['popular'])
async def popular_endpoint(message: types.Message):
    pass


@dp.message(commands=['graph'])
async def graph_endpoint(message: types.Message):
    pass


@dp.message(commands=['history'])
async def history_endpoint(message: types.Message):
    pass


@dp.message(commands=['low'])
async def low_endpoint(message: types.Message):
    pass


@dp.message(commands=['high'])
async def high_endpoint(message: types.Message):
    pass


@dp.message()
async def echo(message: types.Message):
    await message.answer(message.text)
