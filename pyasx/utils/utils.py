import pandas as pd


def df_to_numeric(df):
    for column in df.iloc[:, 1:]:
        tmp_column = [i.replace(',', '').replace('-', '') for i in df[column]]
        df[column] = pd.to_numeric(tmp_column)
    return df


def json_to_df(json):
    base = json['chart']['result'][0]
    timestamp = base['timestamp']
    ohlc = base['indicators']['quote'][0]
    opn = ohlc['open']
    high = ohlc['high']
    low = ohlc['low']
    close = ohlc['close']
    volune = ohlc['volume']

    df = pd.DataFrame({
        'Open': opn,
        'High': high,
        'Low': low,
        'Close': close,
        'Volume': volune
    })
    df.index = pd.to_datetime(timestamp, unit="s")
    df.dropna(inplace=True)
    return df
