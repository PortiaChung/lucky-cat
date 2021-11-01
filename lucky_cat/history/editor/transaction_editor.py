from datetime import datetime

from lucky_cat.history import Session
from lucky_cat.history.position.position import Transactions, TransactionType, StockPositions


class TransactionEditor:
    def __init__(self):
        pass

    @staticmethod
    def close(id: int):
        with Session() as session:
            transaction = session.query(Transactions).get(id)
            type = transaction.type
            if type == TransactionType.stock:
                # TODO: close transaction based on market price
                pass
            else:
                # options are more complex, one transaction can contain multiple OptionPositions rows
                pass


    # remove everything from transaction table, registered triggers will clean up StockPositions & OptionPositions automatically
    @staticmethod
    def clean_up():
        with Session() as session:
            session.query(Transactions).delete()
            session.commit()

    @staticmethod
    def delete(id: int):
        with Session() as session:
            row = session.query(Transactions).get(id)
            session.delete(row)
            session.commit()

    # we may need to prune the transaction table based on some criteria from time to time
    @staticmethod
    def prune():
        pass
