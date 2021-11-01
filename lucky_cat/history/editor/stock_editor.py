import string
from datetime import datetime

from lucky_cat.history import Session
from lucky_cat.history.position.position import Transactions, StockPositions, TransactionType
from sqlalchemy import DATETIME

class StockEditor:
    def __init__(self):
        pass

    @staticmethod
    def buy(ticker: string, open_price: float, shares: int, openDate: datetime):
        transactions = Transactions(ticker=ticker, openDate=openDate, type=TransactionType.stock)
        with Session() as session:
            session.add(transactions)
            session.commit()
            session.refresh(transactions)
        stock_position = StockPositions(transactionId=transactions.id, openPrice=open_price, shares=shares)
        with Session() as session:
            session.add(stock_position)
            session.commit()

    @staticmethod
    def sell(id: int, close_price: float, closeDate: datetime):
        with Session() as session:
            row = session.query(StockPositions).get(id)
            row.closePrice = close_price
            transaction_id = row.transactionId
            session.refresh(row)
            trow = session.query(Transactions).get(transaction_id)
            trow.open = False
            trow.closeDate = closeDate
            trow.earning = (row.closePrice - row.openPrice) * row.shares
            session.commit()

    @staticmethod
    def insert():
        pass

    @staticmethod
    def delete(id: int):
        with Session() as session:
            row = session.query(StockPositions).get(id)
            session.delete(row)
            session.commit()
