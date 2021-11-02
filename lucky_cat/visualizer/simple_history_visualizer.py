import string

from pandas import DataFrame
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from lucky_cat.analyzer.assist_indicators.bollinger_bands import BollingerBands
from lucky_cat.analyzer.assist_indicators.moving_average import MovingAverage
from lucky_cat.analyzer.assist_indicators.rsi import RSI
from lucky_cat.predictor.predictresult import PredictResult


class SimpleHistoryVisualizer:
    def __init__(self, period: int = 180):
        self.period = period

    def visualize(self, ticker: string, history: DataFrame, predictResult: PredictResult):
        pass
        # for visualization, we will only use 180d's data
        fig = make_subplots(rows=4, cols=1, shared_xaxes=True,
                            vertical_spacing=0.03, subplot_titles=[ticker, 'Volume', 'RSI', 'MA'],
                            row_width=[0.1, 0.1, 0.1, 0.7])

        candleStickDF = history.tail(self.period)
        fig.add_trace(go.Candlestick(x=candleStickDF.index,
                                     open=candleStickDF['Open'], high=candleStickDF['High'],
                                     low=candleStickDF['Low'], close=candleStickDF['Close'], name='CandleStick',
                                     opacity=1),
                      row=1, col=1)
        boolingerBand = BollingerBands(history).calculate(20).tail(self.period)
        fig.add_trace(go.Scatter(x=boolingerBand['Date'], y=boolingerBand['DownPrice'], name='Boolinger Down'), row=1,
                      col=1)
        fig.add_trace(go.Scatter(x=boolingerBand['Date'], y=boolingerBand['Price'], name='Boolinger Mid'), row=1, col=1)
        fig.add_trace(go.Scatter(x=boolingerBand['Date'], y=boolingerBand['UpPrice'], name='Boolinger Up'), row=1,
                      col=1)

        # color website: https://community.plotly.com/t/plotly-colours-list/11730
        fig.add_trace(go.Bar(x=candleStickDF.index, y=candleStickDF["Volume"], showlegend=False, yaxis='y2', opacity=1,
                             marker=dict(color='#17becf', colorscale='viridis')
                             ),
                      row=2, col=1)
        rsi = RSI(history).calculate(14).tail(self.period)
        fig.add_trace(go.Scatter(x=rsi['Date'], y=rsi['Indices'], name='rsi'), row=3, col=1)

        movingAverage10d = MovingAverage(history).calculate(10).tail(self.period)
        fig.add_trace(go.Scatter(x=movingAverage10d['Date'], y=movingAverage10d['Price'], name='10d'), row=4, col=1)
        movingAverage30d = MovingAverage(history).calculate(30).tail(self.period)
        fig.add_trace(go.Scatter(x=movingAverage30d['Date'], y=movingAverage30d['Price'], name='30d'), row=4, col=1)

        # disable range slider: https://community.plotly.com/t/go-candlestick-showing-a-second-smaller-graph-not-requested/13342
        fig.update(layout_xaxis_rangeslider_visible=False)

        fig.add_annotation(dict(font=dict(color='LightSteelBlue', size=30),
                                x=0,
                                y=1,
                                align='left',
                                showarrow=False,
                                text=str(predictResult).replace('\n', '<br>'),
                                textangle=0,
                                xanchor='left',
                                xref="paper",
                                yref="paper"))

        fig.show()
