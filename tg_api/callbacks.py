from aiogram import Router, types
from site_api.core import headers, site_api, url
from .utils.states import GetArg
from database.common.models import db, History
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command, CommandStart

router = Router()


@router.message(CommandStart())
async def send_hello(message: types.Message):
    await message.reply("Hi!")


@router.message(Command('quote'))
async def quote_get_arg(message: types.Message, state: FSMContext):
    await state.set_state(GetArg.quote_arg)
    await message.answer('Enter the name of the ticker you are interested in')


@router.message(GetArg.quote_arg)
async def quote_endpoint(message: types.Message, state: FSMContext):
    await state.update_data(quote_arg=message.text)
    await state.clear()
    ticker_name = message.text
    quote = site_api.getter()
    response = quote(url=url,
                     headers=headers,
                     params={"symbol": ticker_name, "function": 'GLOBAL_QUOTE'})

    if not response.ok:
        await message.answer('Error', str(response.status_code))
        exit(1)

    response = response.json()['Global Quote']
    answer = ''

    for key, value in response.items():
        answer += f'{key[4:]}: {value}\n'

    await message.answer(answer)


@router.message(Command('all'))
async def all_endpoint(message: types.Message):
    querystring = 'function=LISTING_STATUS'
    file = types.URLInputFile(url=url + '?' + querystring,
                              headers=headers,
                              filename="listing_status.csv")

    await message.answer_document(file)


@router.message(Command('popular'))
async def popular_endpoint(message: types.Message):
    popular = site_api.getter()
    response = popular(url=url,
                       headers=headers,
                       params={"function": 'TOP_GAINERS_LOSERS'})

    if not response.ok:
        await message.answer('Error', str(response.status_code))
        exit(1)

    response = response.json()['most_actively_traded'][:10]
    answer = ''

    count = 1
    for ticker in response:
        name = ticker['ticker']
        answer += f'{count}. {name}\n'
        count += 1

    await message.answer(answer)


@router.message(Command('graph'))
async def graph_get_arg(message: types.Message, state: FSMContext):
    await state.set_state(GetArg.graph_arg)
    await message.answer('Enter the name of the ticker and time interval:\n'
                         '1min/5min/15min/30min/60min/day/week/month\n\n'
                         'Example: AAPL 15min')


@router.message(GetArg.graph_arg)
async def graph_endpoint(message: types.Message, state: FSMContext):
    await state.update_data(graph_arg=message.text)
    await state.clear()

    ticker_name, interval = message.text.split(' ')
    intervals = ['8hrs', '32hrs', '3day', '10day']

    if interval not in intervals:
        await message.answer('Error, wrong time interval')

    graph_func = site_api.get_graph()
    graph = types.FSInputFile(graph_func(symbol=ticker_name, interval=interval))

    await message.answer_photo(graph)


@router.message(Command('history'))
async def history_endpoint(message: types.Message):
    pass


@router.message(Command('low'))
async def low_endpoint(message: types.Message):
    high = site_api.getter()
    response = high(url=url,
                    headers=headers,
                    params={"function": 'TOP_GAINERS_LOSERS'})

    if not response.ok:
        await message.answer('Error', str(response.status_code))
        exit(1)

    response = response.json()['top_losers'][:10]
    answer = ''

    count = 1
    for ticker in response:
        name = ticker['ticker']
        change = ticker['change_percentage']
        answer += f'{count}. {name}: {change}\n'
        count += 1

    await message.answer(answer)


@router.message(Command('high'))
async def high_endpoint(message: types.Message):
    high = site_api.getter()
    response = high(url=url,
                    headers=headers,
                    params={"function": 'TOP_GAINERS_LOSERS'})

    if not response.ok:
        await message.answer('Error', str(response.status_code))
        exit(1)

    response = response.json()['top_gainers'][:10]
    answer = ''

    count = 1
    for ticker in response:
        name = ticker['ticker']
        change = ticker['change_percentage']
        answer += f'{count}. {name}: {change}\n'
        count += 1

    await message.answer(answer)


@router.message()
async def echo(message: types.Message):
    await message.answer(message.text)

