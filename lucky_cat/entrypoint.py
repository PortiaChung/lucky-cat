import yfinance as yf
from pandas import DataFrame

from common.candlestick.candlestick import CandleStick
import plotly.graph_objects as go

import pandas as pd
import datetime

from lucky_cat.analyzer.hammerline import HammerLine
from lucky_cat.analyzer.hangline import HangLine
from lucky_cat.analyzer.meteorline import MeteorLine
from lucky_cat.analyzer.reversehammerline import ReverseHammerLine
from lucky_cat.analyzer.swallow import Swallow
from lucky_cat.analyzer.swallowext import SwallowExt
from lucky_cat.analyzer.uphugline import UpHugLine
from lucky_cat.analyzer.uppregnantline import UpPregnantLine
from lucky_cat.common.utils.helper import isMonotonic, isMonotonicApproximate
from lucky_cat.news.popular.popular import Popular

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd


# from history.position.position import *
# from history import session

def plot(stock_name, history: DataFrame):
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True,
                        vertical_spacing=0.03, subplot_titles=(stock_name, 'Volume'),
                        row_width=[0.2], specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Candlestick(x=history.index,
                                 open=history['Open'], high=history['High'],
                                 low=history['Low'], close=history['Close'], name='Price', opacity=0.5),
                  row=1, col=1)

    # color website: https://community.plotly.com/t/plotly-colours-list/11730
    fig.add_trace(go.Bar(x=history.index, y=history["Volume"], showlegend=False, yaxis='y2', opacity=0.3,
                         marker=dict(color='#17becf', colorscale='viridis')
                         ),
                  row=1, col=1, secondary_y=True)

    # fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    # fig.layout.yaxis2.showgrid = False
    # fig = go.Figure(
    #     data=[
    #         go.Candlestick(
    #             x=history.index,
    #             open=history['Open'],
    #             high=history['High'],
    #             low=history['Low'],
    #             close=history['Close']
    #         )
    #     ]
    # )
    fig.update(layout_xaxis_rangeslider_visible=False)
    fig.show()


def find_hammer_wire(rh_pop_list):
    print("######## Hammer Wire ########")
    # hammerwire = HammerWire(1 / 5, 3, 1 / 3)
    hammerline = HammerLine(trend_days=5, outlier_ratio=0.3)
    reversehammerline = ReverseHammerLine(trend_days=5, outlier_ratio=0.3)
    meteorline = MeteorLine(trend_days=5)
    hangline = HangLine(trend_days=5)
    uphugline = UpHugLine(trend_days=5)
    uppregnantline = UpPregnantLine(trend_days=5)
    rh_pop_list = ["AAPL"]

    for pop in rh_pop_list:
        try:
            ticker = yf.Ticker(pop)
            history = ticker.history(period="6mo")[:-10]
            print("processing " + pop)
            # if hammerwire.is_up_hammer_wire(history):
            #     print(pop)
            #     plot(pop, history)
            # if hammerline.is_hammer_line(history):
            #     print(pop)
            #     plot(pop, history)
            if uppregnantline.is_up_pregant_line(history):
                print(pop)
                plot(pop, history)
        except Exception as ex:
            print("Hammer Line, ticker: {}, exception: {}".format(pop, ex))


def find_swallow(rh_pop_list):
    print("######## Swallow ########")
    swallow = Swallow(4)
    # rh_pop_list = ['MRNA']
    for pop in rh_pop_list:
        try:
            ticker = yf.Ticker(pop)
            # print(pop)
            history = ticker.history()
            if swallow.is_up_swallow(history) or swallow.is_down_swallow(history):
                print(pop)
                plot(pop, history)
        except Exception as ex:
            print("Swallow, ticker: {}, exception: {}".format(pop, ex))


def find_swallow_ext(rh_pop_list):
    print("######## Swallow Ext ########")
    swallowext = SwallowExt(4, 1 / 2)
    # rh_pop_list = ['FB']
    for pop in rh_pop_list:
        try:
            ticker = yf.Ticker(pop)
            history = ticker.history()
            # print(pop)
            if swallowext.is_up_swallowext(history) or swallowext.is_down_swallowext(history):
                plot(pop, history)
                print(pop)
        except Exception as ex:
            print("Swallow Ext, ticker: {}, exception: {}".format(pop, ex))


def main():
    # open_position = OpenPosition(type="stock", open_price=100.01)
    # session.add(open_position)
    # session.commit()

    # print("here is the start of program")
    # import pymysql.cursors
    # connection = pymysql.connect(host='localhost',
    #                              user='root',
    #                              password='password',
    #                              # database='db',
    #                              cursorclass=pymysql.cursors.DictCursor)
    # with connection:
    #     with connection.cursor() as cursor:
    #         # Create a new record
    #         # sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
    #         # cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
    #         sql = "show databases"
    #         results = cursor.execute(sql)
    #         print(cursor.fetchall())

    rh_pop_list = Popular.get_robinhood_populars()

    # print(yf.Ticker("AMD").history().iloc[-1])
    # exit(0)

    find_hammer_wire(rh_pop_list)
    # find_swallow(rh_pop_list)
    # find_swallow_ext(rh_pop_list)

    # # do history stats analysis
    # hammerwire = HammerWire(1 / 5, 3, 1 / 3)
    # # candidates = ['UBER', 'TSLA', 'COIN', 'NIO', 'F', 'BABA', 'XPEV', 'NOK', 'DIS', 'PFE']
    # candidates = ['XPEV']
    # for candidate in candidates:
    #     ticker = yf.Ticker(candidate)
    #     shape = ticker.history('1y').shape
    #     print("candidate: {}, shape is: {}".format(candidate, shape))
    #     for i in range(0, shape[0] - 7):
    #         # print("iterate: {}".format(i))
    #         history = ticker.history(period='{}'.format('1y')).iloc[0:shape[0] - i]
    #         if hammerwire.is_hammer_wire(history):
    #             print(history.tail(1).index)
    #             history = ticker.history(period='{}'.format('1y')).iloc[max(shape[0] - i - 15, 0) : shape[0] - i + 15]
    #             fig = go.Figure(
    #                 data=[
    #                     go.Candlestick(
    #                         x=history.index,
    #                         open=history['Open'],
    #                         high=history['High'],
    #                         low=history['Low'],
    #                         close=history['Close']
    #                     )
    #                 ]
    #             )
    #             fig.show()

    # ticker = yf.Ticker('SNOW')
    # print(ticker.info)
    # df = ticker.history(period='1y').tail(5)
    # print(df)

    # close_prices_array = []
    # for index, row in df.iterrows():
    #     print("open: {}, close: {}".format(row['Open'], row['Close']))
    #     close_prices_array += row['Close']
    # print(isMonotonic(close_prices_array))

    pass
    # print("Day 1")
    # msft = yf.Ticker("MSFT")
    # # print(msft.info)
    # hist = msft.history(period="1mo", interval="1d")
    # print(hist.columns)
    # # print(hist.tail(10))
    # # print(hist.head(1))
    # print("##################")
    # print(hist.tail(1).to_string())
    # print("##################")
    # last = hist.tail(1)
    # print(last["Close"].values[0])
    # candleStick = CandleStick(
    #     last["Open"].values[0],
    #     last["Close"].values[0],
    #     last["Low"].values[0],
    #     last["High"].values[0]
    # )
    #
    # print(candleStick)
    #
    # print(type(hist.index))
    # print(type(hist.Open))
    #
    # print(hist.Open)
    #
    # print(hist.shape)
    #
    #
    # fig = go.Figure(
    #     data=[
    #         go.Candlestick(
    #             x=hist.index,
    #             open=hist['Open'],
    #             high=hist['High'],
    #             low=hist['Low'],
    #             close=hist['Close']
    #         )
    #     ]
    # )
    #
    # print(type(hist.index))
    #
    # # fig.show()
    #
    # # print(last["Open"])
    # from pyrh import Robinhood
    #
    # # rh = Robinhood()
    # # rh.login(username="tianr.zhou@gmail.com", password="bravetradingbot")
    # # rh.print_quote("AAPL")
    #
    # rh_pop_list = Popular.get_robinhood_populars()
    # for pop in rh_pop_list:
    #     ticker = yf.Ticker(pop)
    #     print(ticker.info)


if __name__ == "__main__":
    main()
