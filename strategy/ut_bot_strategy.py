# TODO: complete this asap
import numpy as np
import talib as ta
from indicators import HA


def UT_Bot_Alerts(df, sensitivity, atr_period, heikin_ashi=False):
    close = df['Close']
    if heikin_ashi:
        src = HA(df, )
    else:
        src = close

    xATR = ta.ATR(src, atr_period)
    nLoss = sensitivity * xATR

    xATRTrailingStop = np.zeros(len(src))
    pos = np.zeros(len(src))

    for i in range(1, len(src)):
        if src[i] > src[i - 1] and src[i - 1] > xATRTrailingStop[i - 1]:
            xATRTrailingStop[i] = max(xATRTrailingStop[i - 1], src[i] - nLoss)
        elif src[i] < src[i - 1] and src[i - 1] < xATRTrailingStop[i - 1]:
            xATRTrailingStop[i] = min(xATRTrailingStop[i - 1], src[i] + nLoss)
        elif src[i] > src[i - 1]:
            xATRTrailingStop[i] = src[i] - nLoss
        else:
            xATRTrailingStop[i] = src[i] + nLoss

        if src[i] > xATRTrailingStop[i] and src[i - 1] < xATRTrailingStop[i - 1]:
            pos[i] = 1
        elif src[i] < xATRTrailingStop[i] and src[i - 1] > xATRTrailingStop[i - 1]:
            pos[i] = -1
        else:
            pos[i] = pos[i - 1]

    ema = ta.EMA(src, 1)
    above = np.zeros(len(src))
    below = np.zeros(len(src))

    for i in range(1, len(src)):
        if ema[i] > xATRTrailingStop[i]:
            above[i] = 1
        if ema[i] < xATRTrailingStop[i]:
            below[i] = -1

    buy = np.zeros(len(src))
    sell = np.zeros(len(src))

    for i in range(1, len(src)):
        if src[i] > xATRTrailingStop[i] and above[i] == 1:
            buy[i] = 1
        if src[i] < xATRTrailingStop[i] and below[i] == -1:
            sell[i] = -1

    return xATRTrailingStop, pos, buy, sell
