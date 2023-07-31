from database.common.models import db, History
from database.core import crud
from site_api.core import headers, querystring, site_api, url

db_write = crud.create()
db_read = crud.retrieve()

test = site_api.get_test()

response = test(method="GET", url=url, headers=headers, querystring=querystring)
if isinstance(response, int):
    #TODO вывод ошибки
    exit(-1)

response = response.json()['Global Quote']

data = [
    {
        "symbol": response.get("01. symbol"),
        "open": response.get("02. open"),
        "high": response.get("03. high"),
        "low": response.get("04. low"),
        "price": response.get("05. price"),
        "volume": response.get("06. volume"),
        "latest_trading_day": response.get("07. latest trading day"),
        "previous_close": response.get("08. previous close"),
        "change": response.get("09. change"),
        "change_percent": response.get("10. change percent")
    }
]

db_write(db, History, data)

retrieved = db_read(db, History)
