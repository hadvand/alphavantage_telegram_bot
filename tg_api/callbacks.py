from aiogram import Router, types
from site_api.core import headers, site_api, url
from .utils.states import GetArg
from database.core import crud, db, History
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command, CommandStart
import os

router = Router()

db_write = crud.create()
db_read = crud.retrieve()


@router.message(CommandStart())
async def send_hello(message: types.Message):
    """Welcoming message"""
    await message.reply('Hi!')


@router.message(Command('quote'))
async def quote_get_arg(message: types.Message, state: FSMContext):
    """First state of 'quote' endpoint"""
    await state.set_state(GetArg.quote_arg)
    await message.answer('Enter the name of the ticker you are interested in')


@router.message(GetArg.quote_arg)
async def quote_endpoint(message: types.Message, state: FSMContext):
    """Last state of 'quote' endpoint where you get the information about desired ticker"""
    await state.update_data(quote_arg=message.text)
    await state.clear()
    ticker_name = message.text
    quote = site_api.getter()
    response = quote(url=url,
                     headers=headers,
                     params={'symbol': ticker_name, 'function': 'GLOBAL_QUOTE'})

    if not response.ok:
        await message.answer('Error', str(response.status_code))

    response = response.json()['Global Quote']
    answer = ''

    if len(response.items()) == 0:
        await message.answer('You may have entered an invalid ticker name \nCanceling operation...')
        return

    for key, value in response.items():
        answer += f'{key[4:]}: {value}\n'

    data = [{'command': '/quote', 'ticker': ticker_name.upper(), 'user': message.from_user.id}]
    db_write(db, History, data)

    await message.answer(answer)


@router.message(Command('all'))
async def all_endpoint(message: types.Message):
    """"Endpoint to get a list of all available tickers"""
    querystring = 'function=LISTING_STATUS'
    file = types.URLInputFile(url=url + '?' + querystring,
                              headers=headers,
                              filename='listing_status.csv')

    data = [{'command': '/all', 'ticker': '', 'user': message.from_user.id}]
    db_write(db, History, data)

    await message.answer_document(file)


@router.message(Command('popular'))
async def popular_endpoint(message: types.Message):
    """Endpoint to get top-10 most popular tickers of the day"""
    popular = site_api.getter()
    response = popular(url=url,
                       headers=headers,
                       params={'function': 'TOP_GAINERS_LOSERS'})

    if not response.ok:
        await message.answer('Error', str(response.status_code))

    response = response.json()['most_actively_traded'][:10]
    answer = ''

    count = 1
    for ticker in response:
        name = ticker['ticker']
        answer += f'{count}. {name}\n'
        count += 1

    data = [{'command': '/popular', 'ticker': '', 'user': message.from_user.id}]
    db_write(db, History, data)

    await message.answer(answer)


@router.message(Command('graph'))
async def graph_get_arg(message: types.Message, state: FSMContext):
    """First state of 'graph' endpoint"""
    await state.set_state(GetArg.graph_arg)
    await message.answer('Enter the name of the ticker and time interval:\n'
                         '8hrs/32hrs/3days/10days\n\n'
                         'Example: AAPL 32hrs')


@router.message(GetArg.graph_arg)
async def graph_endpoint(message: types.Message, state: FSMContext):
    """Last state of the endpoint to get a graph of price changes of the desired"""
    await state.update_data(graph_arg=message.text)
    await state.clear()

    if len(message.text.split(' ')) != 2:
        await message.answer('Only one argument was entered \nCanceling operation...')
        return

    ticker_name, interval = message.text.split(' ')
    intervals = ['8hrs', '32hrs', '3days', '10days']

    if interval not in intervals:
        await message.answer('Error, wrong time interval')

    graph_func = site_api.get_graph()
    graph_name = graph_func(symbol=ticker_name, interval=interval)

    if graph_name is None:
        await message.answer('You may have entered an invalid ticker name \nCanceling operation...')
        return

    graph = types.FSInputFile(graph_name)

    data = [{'command': '/graph', 'ticker': ticker_name.upper(), 'user': message.from_user.id}]
    db_write(db, History, data)

    await message.answer_photo(graph)

    for file in os.listdir():   # removing png file after sending it
        if file.endswith('.png'):
            os.remove(file)


@router.message(Command('history'))
async def history_endpoint(message: types.Message):
    """Endpoint to get a history of previously used commands"""
    retrieved = db_read(db, message.from_user.id, History, History.created_at, History.command, History.ticker)
    answer = ''
    for element in retrieved:
        answer += f'{element.created_at}: {element.command} {element.ticker}\n'

    data = [{'command': '/history', 'ticker': '', 'user': message.from_user.id}]
    db_write(db, History, data)

    if answer == '':
        answer = f'The history is empty.'

    await message.answer(answer)


@router.message(Command('low'))
async def low_endpoint(message: types.Message):
    """Endpoint to get top losers of today"""
    high = site_api.getter()
    response = high(url=url,
                    headers=headers,
                    params={'function': 'TOP_GAINERS_LOSERS'})

    if not response.ok:
        await message.answer('Error', str(response.status_code))

    response = response.json()['top_losers'][:10]
    answer = ''

    count = 1
    for ticker in response:
        name = ticker['ticker']
        change = ticker['change_percentage']
        answer += f'{count}. {name}: {change}\n'
        count += 1

    data = [{'command': '/low', 'ticker': '', 'user': message.from_user.id}]
    db_write(db, History, data)

    await message.answer(answer)


@router.message(Command('high'))
async def high_endpoint(message: types.Message):
    """Endpoint to get top gainers of today"""
    high = site_api.getter()
    response = high(url=url,
                    headers=headers,
                    params={'function': 'TOP_GAINERS_LOSERS'})

    if not response.ok:
        await message.answer('Error', str(response.status_code))

    response = response.json()['top_gainers'][:10]
    answer = ''

    count = 1
    for ticker in response:
        name = ticker['ticker']
        change = ticker['change_percentage']
        answer += f'{count}. {name}: {change}\n'
        count += 1

    data = [{'command': '/high', 'ticker': '', 'user': message.from_user.id}]
    db_write(db, History, data)

    await message.answer(answer)
