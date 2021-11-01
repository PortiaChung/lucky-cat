from pandas import DataFrame
from lucky_cat.analyzer.basicanalyzer import BasicAnalyzer
from lucky_cat.predictor.predictresult import PredictResult
from abc import abstractmethod

class BasePredictor:
    def __init__(self):
        pass

    @abstractmethod
    def predict(self, data: DataFrame, analyzer: BasicAnalyzer) -> PredictResult:
        pass