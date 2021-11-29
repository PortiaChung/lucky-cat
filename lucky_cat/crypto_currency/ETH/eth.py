import datetime

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
from lucky_cat.crypto_currency.data_loader import DataLoader, CurrencyType, TimeRange
from lucky_cat.crypto_currency.data_loader_v2 import DataLoaderV2
from lucky_cat.predictor.simplehistorypredictor import SimpleHistoryPredictor
from lucky_cat.visualizer.simple_history_visualizer import SimpleHistoryVisualizer


def main():
    trend_days = 10
    analyzers_list = [DownHugLine(trend_days), DownPregantLine(trend_days), DownSwallow(trend_days),
                      DownSwallowExt(trend_days), HammerLine(trend_days), HangLine(trend_days),
                      MeteorLine(trend_days), ReverseHammerLine(trend_days), UpHugLine(trend_days),
                      UpPregnantLine(trend_days), UpSwallow(trend_days), UpSwallowExt(trend_days)]
    simpleHistoryPredictor = SimpleHistoryPredictor()
    simpleHistoryVisualizer = SimpleHistoryVisualizer()

    # analyzers_list = [HammerLine(trend_days)]
    # data_loader = DataLoader()
    # history = data_loader.load(CurrencyType.ETH, TimeRange.day, 1000)
    data_loader_v2 = DataLoaderV2()
    history = data_loader_v2.load('ETHUSD', '1d', datetime.datetime(2019, 1, 1, 0, 0),
                               datetime.datetime(2021, 11, 7, 0, 0), 1000)

    for analyzer in analyzers_list:
        predictResult = simpleHistoryPredictor.predict(history, analyzer)
        print(predictResult)
        simpleHistoryVisualizer.visualize('ETH', history, predictResult)



if __name__ == "__main__":
    main()