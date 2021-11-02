from pandas import DataFrame

from lucky_cat.analyzer.basicanalyzer import BasicAnalyzer
from lucky_cat.predictor.basepredictor import BasePredictor
from overrides import overrides

from lucky_cat.predictor.predictresult import PredictResult
from datetime import datetime, timedelta


class SimpleHistoryPredictor(BasePredictor):
    def __init__(self, trend_days: int = 6):
        super().__init__()
        # use this range to monitor price directions after shape detected
        self.trend_days = trend_days

    @overrides
    def predict(self, data: DataFrame, analyzer: BasicAnalyzer) -> PredictResult:
        data_size = data.shape[0]
        # we won't predict on data less than 180d
        if data_size < 180:
            return -1

        # we will analyze 10 year's data at most
        start = max(30, data_size - 15 - 3650)
        occurence = 0

        oscillate_points = []
        meet_points = []
        violate_points = []
        # candidate_data = data[30:-15]
        for i in range(start, data_size - 15):
            if analyzer.analyze(data.iloc[:i]):
                occurence += 1
                # analyze data of next week(7 day?)
                anchor_point = data.iloc[i - 1]
                # print("find shape " + analyzer.name)
                anchor_point_close = anchor_point['Close']
                anchor_point_date = anchor_point['Date']
                following_prices = []
                for j in range(1, self.trend_days + 1):
                    following_prices.append(data.iloc[i + j]['Close'])
                following_min = min(following_prices)
                following_max = max(following_prices)
                # TODO: need to validate this
                # d = datetime.today() - timedelta(days=data_size - i)
                # price is oscillating, no obvious trend
                if abs(following_min - anchor_point_close) / anchor_point_close < 0.01 and abs(
                        following_max - anchor_point_close) / anchor_point_close < 0.01:
                    oscillate_points.append(anchor_point_date)
                elif analyzer.upward:
                    if following_max > anchor_point_close and (
                            following_max - anchor_point_close) / anchor_point_close > 0.03:
                        meet_points.append(anchor_point_date)
                    else:
                        violate_points.append(anchor_point_date)
                else:
                    if following_min < anchor_point_close and (
                            anchor_point_close - following_min) / anchor_point_close > 0.03:
                        meet_points.append(anchor_point_date)
                    else:
                        violate_points.append(anchor_point_date)

        return PredictResult(analyzer.name, occurence, oscillate_points, meet_points, violate_points)
