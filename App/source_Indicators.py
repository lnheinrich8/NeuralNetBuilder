import pandas as pd

def rsi(ohlc, period = 14):
    delta = ohlc["close"].diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    _gain = up.ewm(com=(period - 1), min_periods=period).mean()
    _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
    RS = _gain / _loss
    return pd.Series(100 - (100 / (1 + RS)), name="RSI")

def sma(ohlc, period = 50):
    return pd.Series(ohlc["close"].rolling(window=period, min_periods=period).mean(), name="SMA")

def ema(ohlc, period = 10):
    return pd.Series(ohlc["close"].ewm(span=period, adjust=False).mean(), name="EMA")


# this will grow with every addition of an indicator
def get_indicator_function_dictiary():

    function_dictionary = {
        'SMA': sma,
        'EMA': ema
    }

    return function_dictionary

# this will grow with every addition of an indicator
def get_indicator_list():
    indicator_list = ['SMA', 'EMA']
    return indicator_list
