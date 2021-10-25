from pandas import DataFrame
from abc import abstractmethod

from lucky_cat.common.utils.helper import isIncTrend, isDecTrend


class BasicAnalyzer:
    # trend_days & outlier_ratio are necessary for all analyzers
    def __init__(self, trend_days: int = 10, outlier_ratio: float = 0.3):
        self.trend_days = trend_days
        self.outlier_ratio = outlier_ratio

    def incTrend(self, trend_df: DataFrame) -> bool:
        history_close_prices = []
        for index, row in trend_df.iterrows():
            history_close_prices.append(row['Close'])
        return isIncTrend(history_close_prices, self.outlier_ratio)

    def decTrend(self, trend_df: DataFrame) -> bool:
        history_close_prices = []
        for index, row in trend_df.iterrows():
            history_close_prices.append(row['Close'])
        return isDecTrend(history_close_prices, self.outlier_ratio)

    def isVolumeAmplifed(self, history: DataFrame, expect_ratio: float):
        today_volume = history.iloc[-1]['Volume']
        volume_df = history.iloc[:-1].tail(self.trend_days)
        history_volumes = []
        for index, row in volume_df.iterrows():
            history_volumes.append(row['Volume'])
        avg_volumes = sum(history_volumes) / len(history_volumes)
        if avg_volumes * expect_ratio > today_volume:
            return False
        return True

    @abstractmethod
    def isShapeDetected(self, history: DataFrame) -> bool:
        pass

    @abstractmethod
    def analyze(self, history: DataFrame) -> bool:
        pass

