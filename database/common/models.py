from datetime import datetime
import peewee as pw

db = pw.SqliteDatabase('database.db')


class ModelBase(pw.Model):
    created_at = pw.DateField(default=datetime.now())

    class Meta:
        database = db


class History(ModelBase):
    symbol = pw.TextField()
    open = pw.TextField()
    high = pw.TextField()
    low = pw.TextField()
    price = pw.TextField()
    volume = pw.TextField()
    latest_trading_day = pw.TextField()
    previous_close = pw.TextField()
    change = pw.TextField()
    change_percent = pw.TextField()
