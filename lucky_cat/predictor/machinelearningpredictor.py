from pandas import DataFrame

from lucky_cat.analyzer.basicanalyzer import BasicAnalyzer
from lucky_cat.predictor.basepredictor import BasePredictor
from overrides import overrides


# TODO: use machine learning to predict
class MachineLearningPredictor(BasePredictor):
    def __init__(self):
        super().__init__()

    @overrides
    def predict(self, data: DataFrame, analyzer: BasicAnalyzer) -> float:
        return 0.0