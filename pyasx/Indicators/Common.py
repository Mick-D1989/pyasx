class Common:
    def __init__(self, ohlcv_df):
        self.data = ohlcv_df

    def hlc3(self):
        return (self.data['High'] + self.data['Low'] + self.data['Close']) / 3

    def vwap(self):
        """Volume Weighted Average Price
        Calculation:
            average_price = (high + low + close)/3
            vwap = (volume * average_price) / volume
        :return: vwap
        :rtype: Pandas Series
        """
        # Calculate the daily volume weighted average price
        return (self.data['Volume'] * self.hlc3()) / self.data['Volume']

    def sma(self, window=7, **kwargs):
        if 'series_type' in kwargs and kwargs['series_type'] in self.data:
            series = self.data[kwargs['series_type']]
        elif 'data' in kwargs:
            series = kwargs['data']
        else:
            series = self.data['Close']
        return series.rolling(window).mean()

    def ema(self, window=7, **kwargs):
        if 'series_type' in kwargs and kwargs['series_type'] in self.data:
            series = self.data[kwargs['series_type']]
        elif 'data' in kwargs:
            series = kwargs['data']
        else:
            series = self.data['Close']
        return series.ewm(span=window, adjust=False).mean()
