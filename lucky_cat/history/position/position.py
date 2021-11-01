from sqlalchemy import Column, Integer, String, FLOAT, DATETIME, Enum, Boolean, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from lucky_cat.history import base
from sqlalchemy.sql import func
import enum

class TransactionType(enum.Enum):
    stock = 1
    option = 2

# we assume that each transaction must be make as a whole, don't support close partial transactions
class Transactions(base.Base):
    __tablename__ = 'transactions'
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True)
    openDate = Column('open_date', DATETIME(timezone=True), server_default=func.now())
    closeDate = Column('close_date', DATETIME(timezone=True), server_default=func.now())
    # category = Column('category', Enum(TransactionType))
    ticker = Column('ticker', String(32))
    type = Column('type', Enum(TransactionType))
    open = Column('open', Boolean, default=True)
    earning = Column('earning', DECIMAL(18, 2), default=0)
    earning_percent = Column('earning_percent', DECIMAL(18, 2), default=0)

    stockPositions = relationship('StockPositions', passive_deletes=True, backref='transactions')
    optionPositions = relationship('OptionPositions', passive_deletes=True, backref='transactions')

class StockPositions(base.Base):
    __tablename__ = 'stock_positions'
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True)
    transactionId = Column('transaction_id', Integer, ForeignKey('transactions.id', ondelete='CASCADE'))

    openPrice = Column('open_price', DECIMAL(18, 2))
    shares = Column('shares', Integer)
    closePrice = Column('close_price', DECIMAL(18, 2), default=0)

class OptionType(enum.Enum):
    buy_call = 1
    buy_put = 2
    sell_call = 3
    sell_put = 4

class OptionPositions(base.Base):
    __tablename__ = 'option_positions'
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True)
    transactionId = Column('transaction_id', Integer, ForeignKey('transactions.id', ondelete='CASCADE'))

    # optionType = Column('option_type', Enum(OptionType))
    openCashflow = Column('open_cashflow', DECIMAL(18, 2))
    hand = Column('hand', Integer)
    strikePrice = Column('strike_price', DECIMAL(18, 2))
    expirationDate = Column('expiration_date', DATETIME(timezone=True), server_default=func.now())
    closeCashflow = Column('close_cashflow', DECIMAL(18, 2), default=0)
