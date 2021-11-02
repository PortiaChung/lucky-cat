import datetime
import string
import pandas as pd
import os.path
import requests
from pandas_datareader import data

from lucky_cat.news.popular import package_directory


class Popular:
    SP500File = '{}/generated/sp500list'.format(package_directory)
    NASDAQ100File = '{}/generated/nasdaq100list'.format(package_directory)
    DOW30File = '{}/generated/dow30list'.format(package_directory)

    def __init__(self):
        pass

    @staticmethod
    def get_nasdaq_100_company_list():
        return Popular.get_company_list(Popular.NASDAQ100File)

    @staticmethod
    def get_sp_500_company_list():
        return Popular.get_company_list(Popular.SP500File)

    @staticmethod
    def get_dow_30_company_list():
        return Popular.get_company_list(Popular.DOW30File)

    @staticmethod
    def get_raw_symbols_list(path: string) -> list:
        if path == Popular.SP500File:
            payload = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
            df = payload[0]
            return df['Symbol'].values.tolist()
        elif path == Popular.NASDAQ100File:
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}
            res = requests.get("https://api.nasdaq.com/api/quote/list-type/nasdaq100", headers=headers)
            rows = res.json()['data']['data']['rows']
            return [row['symbol'] for row in rows]
        elif path == Popular.DOW30File:
            payload = pd.read_html('https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average')
            df = payload[1]
            return df['Symbol'].values.tolist()

    @staticmethod
    def refresh_company_list(path: string):
        symbols = Popular.get_raw_symbols_list(path)
        boost_list = []
        for symbol in symbols:
            try:
                market_cap = data.get_quote_yahoo(symbol)['marketCap'].values[0]
                boost_list.append((symbol, market_cap))
                print(len(boost_list))
            except Exception:
                print("Encounter error when getting value for ticket: {}".format(symbol))

        sorted_list = sorted(boost_list, key=lambda x: -x[1])
        final_list = [item[0] for item in sorted_list]
        print(final_list)
        with open(path, mode='w') as f:
            f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + '\n')
            f.write('\n'.join(final_list))

    @staticmethod
    def refresh_nasdaq_100_company_list():
        pass

    @staticmethod
    def refresh_dow_30_company_list():
        pass

    @staticmethod
    def refresh_sp_500_company_list():
        """
        retrieve s&p 500 company list and sort by market cap, save list to file, this function is very slow, we will
        only refresh the list monthly
        """
        payload = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        df = payload[0]
        raw_list = df['Symbol'].values.tolist()
        boost_list = []
        for symbol in raw_list:
            try:
                market_cap = data.get_quote_yahoo(symbol)['marketCap'].values[0]
                boost_list.append((symbol, market_cap))
                print(len(boost_list))
            except Exception:
                print("Encounter error when getting value for ticket: {}".format(symbol))

        sorted_list = sorted(boost_list, key=lambda x: -x[1])
        final_list = [item[0] for item in sorted_list]
        print(final_list)
        with open(Popular.SP500File, mode='w') as f:
            f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") + '\n')
            f.write('\n'.join(final_list))

    @staticmethod
    def get_company_list(path: string):
        if not os.path.exists(path):
            Popular.refresh_company_list(path)
        companies = []
        with open(path) as f:
            timestamp_str = f.readline().strip()
            timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
            now = datetime.datetime.now()
            if (now - timestamp) > datetime.timedelta(days=30):
                Popular.refresh_company_list(path)
            ticker = f.readline().strip()
            while (ticker):
                companies.append(ticker)
                ticker = f.readline().strip()
        return companies


def main():
    # Test company list generation and sorting
    print(Popular.get_sp_500_company_list())
    # print(Popular.get_nasdaq_100_company_list())
    # print(Popular.get_dow_30_company_list())
    print(package_directory)
    pass


if __name__ == "__main__":
    main()
