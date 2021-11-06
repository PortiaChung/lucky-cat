import yfinance as yf
from lucky_cat.analyzer.downhugline import DownHugLine
from lucky_cat.analyzer.downpregantline import DownPregantLine
from lucky_cat.analyzer.downswallow import DownSwallow
from lucky_cat.analyzer.downswallowext import DownSwallowExt
from lucky_cat.analyzer.hammerline import HammerLine
from lucky_cat.analyzer.hangline import HangLine
from lucky_cat.analyzer.meteorline import MeteorLine
from lucky_cat.analyzer.reversehammerline import ReverseHammerLine
from lucky_cat.analyzer.uphugline import UpHugLine
from lucky_cat.analyzer.uppregnantline import UpPregnantLine
from lucky_cat.analyzer.upswallow import UpSwallow
from lucky_cat.analyzer.upswallowext import UpSwallowExt
from lucky_cat.news.popular.popular import Popular
from lucky_cat.predictor.simplehistorypredictor import SimpleHistoryPredictor
from lucky_cat.visualizer.simple_history_visualizer import SimpleHistoryVisualizer


def main():
    symbols_list = Popular.get_nasdaq_100_company_list()
    trend_days = 10
    analyzers_list = [DownHugLine(trend_days), DownPregantLine(trend_days), DownSwallow(trend_days),
                      DownSwallowExt(trend_days), HammerLine(trend_days), HangLine(trend_days),
                      MeteorLine(trend_days), ReverseHammerLine(trend_days), UpHugLine(trend_days),
                      UpPregnantLine(trend_days), UpSwallow(trend_days), UpSwallowExt(trend_days)]
    simpleHistoryPredictor = SimpleHistoryPredictor()
    simpleHistoryVisualizer = SimpleHistoryVisualizer()
    for symbol in symbols_list:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="5y")
        dates = []
        for index, row in history.iterrows():
            dates.append(index)
        history['Date'] = dates
        for analyzer in analyzers_list:
            if analyzer.analyze(history):
                print(symbol)
                predictResult = simpleHistoryPredictor.predict(history, analyzer)
                simpleHistoryVisualizer.visualize(symbol, history, predictResult)


if __name__ == "__main__":
    main()
