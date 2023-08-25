from database.common.models import db, History
from database.core import crud
from site_api.core import headers, site_api, url
from tg_api.callbacks import dp


# db_write = crud.create()
# db_read = crud.retrieve()

dp.start_polling(dp, skip_updates=True)
