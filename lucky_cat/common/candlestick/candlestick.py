class CandleStick:
    def __init__(self, open, close, high, low):
        self.open = open
        self.close = close
        self.high = high
        self.low = low

    def __str__(self):
        return "Candle stick def: open -> {open}, close -> {close}, low -> {low}, high -> {high}".format(
            open=self.open, close=self.close, low=self.low, high=self.high
        )