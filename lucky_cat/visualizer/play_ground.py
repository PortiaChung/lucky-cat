import plotly.graph_objects as go
import yfinance as yf

from lucky_cat.analyzer.assist_indicators.bollinger_bands import BollingerBands
from lucky_cat.analyzer.assist_indicators.moving_average import MovingAverage
from plotly.subplots import make_subplots

from lucky_cat.analyzer.assist_indicators.rsi import RSI


def main():
    print("Test ploting")
    # fig = go.Figure(data=go.Scatter(x=[1,2,3], y=[3,4,5]))
    # fig.show()

    ticker = yf.Ticker('MSFT')
    history = ticker.history(period="1y")
    dates = []
    vols = []
    for index, row in history.iterrows():
        dates.append(index)
        vols.append(row['Close'])
    history['Date'] = dates

    # fig = go.Figure(data=go.Scatter(x=history['Date'], y=history['Close']))
    # fig.show()

    # fig = make_subplots(rows=1, cols=1, shared_xaxes=True, shared_yaxes=True,
    #                     vertical_spacing=0.03, subplot_titles=['Moving Average'])

    # movingAverage10d = MovingAverage(history).calculate(10)
    # fig.add_trace(go.Scatter(x=movingAverage10d['Date'], y=movingAverage10d['Price'], name='10d'))
    #
    # movingAverage30d = MovingAverage(history).calculate(30)
    # fig.add_trace(go.Scatter(x=movingAverage30d['Date'], y=movingAverage30d['Price'], name='30d'))
    # fig.show()

    # fig = make_subplots(rows=1, cols=1, shared_xaxes=True, shared_yaxes=True,
    #                     vertical_spacing=0.03, subplot_titles=['Boolinger Bands'])

    # boolingerBand = BollingerBands(history).calculate(20)
    # fig.add_trace(go.Scatter(x=boolingerBand['Date'], y=boolingerBand['DownPrice'], name='Down'))
    # fig.add_trace(go.Scatter(x=boolingerBand['Date'], y=boolingerBand['Price'], name='Mid'))
    # fig.add_trace(go.Scatter(x=boolingerBand['Date'], y=boolingerBand['UpPrice'], name='Up'))
    # fig.show()

    fig = make_subplots(rows=1, cols=1, shared_xaxes=True, shared_yaxes=True,
                        vertical_spacing=0.03, subplot_titles=['RSI'])

    rsi = RSI(history).calculate(14)
    fig.add_trace(go.Scatter(x=rsi['Date'], y=rsi['Indices'], name='rsi'))
    fig.show()

if __name__ == "__main__":
    main()