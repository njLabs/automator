import pandas as pd
import talib


def has_cross(close_prices, ema_periods):
    emas = pd.DataFrame({f'EMA{period}': talib.EMA(close_prices.values, timeperiod=period) for period in ema_periods}, index=close_prices.index)
    above = (emas.diff() > 0).all(axis=1)
    below = (emas.diff() < 0).all(axis=1)
    above_groups = above.groupby((above != above.shift()).cumsum())
    below_groups = below.groupby((below != below.shift()).cumsum())
    result = pd.Series(0, index=close_prices.index)
    result.iloc[above_groups.tail(1).index] = 1
    result.iloc[below_groups.tail(1).index] = 0
    return result
