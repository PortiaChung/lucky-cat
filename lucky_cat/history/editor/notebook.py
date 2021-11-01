from stock_editor import StockEditor
from transaction_editor import TransactionEditor
from sqlalchemy import DATETIME
import datetime
def main():
    # Examples of stock trading
    StockEditor.buy('DAL', 39.10, 50, datetime.datetime.strptime("10/29/2021 05:50:18", "%m/%d/%Y %H:%M:%S"))
    # StockEditor.sell(1, 45.1, datetime.datetime.strptime("10/31/2021 09:36:18", "%m/%d/%Y %H:%M:%S"))

    # Clean up all transactions
    # TransactionEditor.clean_up()
    # Delete a single transaction based on id
    # TransactionEditor.delete(1)

    # Delete single row in Stock table, may cause inconsistency
    # StockEditor.delete(1)
    pass


if __name__=="__main__":
    main()
