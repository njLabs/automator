import pandas as pd


class PivotPoints:
    def __int__(self, df):
        self.df = df
        self.high = self.df['High']
        self.low = self.df['Low']
        self.close = self.df['Close']
        self.pivot = (self.high + self.low + self.close) / 3
        self.df['self.pivot'] = pd.DataFrame(round(self.pivot, 2))

    def classic_woodie_pivots(self):
        """calculate Classic/ Woodie pivot points (confirmed with tradingView)"""
        self.df['r1'] = pd.DataFrame(round(2 * self.pivot - self.low, 2))
        self.df['r2'] = pd.DataFrame(round(self.pivot + (self.high-self.low), 2))
        self.df['r3'] = pd.DataFrame(round(self.pivot + 2*(self.high-self.low), 2))
        self.df['s1'] = pd.DataFrame(round(2*self.pivot-self.high, 2))
        self.df['s2'] = pd.DataFrame(round(self.pivot - (self.high-self.low), 2))
        self.df['s3'] = pd.DataFrame(round(self.pivot - 2*(self.high-self.low), 2))
        return self.df

    def fibonacci_pivots(self):
        """calculating pivot point using fibonacci (confirmed with tradingView)"""
        self.df['self.pivot'] = pd.DataFrame(round(self.pivot, 2))
        self.df['r1'] = pd.DataFrame(round(self.pivot + (0.382 * (self.high - self.low)), 2))
        self.df['r2'] = pd.DataFrame(round(self.pivot + (0.618 * (self.high - self.low)), 2))
        self.df['r3'] = pd.DataFrame(round(self.pivot + (1 * (self.high - self.low)), 2))
        self.df['s1'] = pd.DataFrame(round(self.pivot - (0.382 * (self.high - self.low)), 2))
        self.df['s2'] = pd.DataFrame(round(self.pivot - (0.618 * (self.high - self.low)), 2))
        self.df['s3'] = pd.DataFrame(round(self.pivot - (1 * (self.high - self.low)), 2))
        return self.df
    
    def camarilla_pivots(self):
        """calculating pivot point using Camarilla (tradingCampus) (confirmed with tradingView)"""
        self.df['self.pivot'] = pd.DataFrame(round(self.pivot, 2))
        self.df['r1'] = pd.DataFrame(round(self.close + (self.high - self.low) * 0.083, 2))
        self.df['r2'] = pd.DataFrame(round(self.close + ((self.high - self.low) * 0.17), 2))
        self.df['r3'] = pd.DataFrame(round(self.close + ((self.high - self.low) * 0.27), 2))
        self.df['s1'] = pd.DataFrame(round(self.close - ((self.high - self.low) * 0.083), 2))
        self.df['s2'] = pd.DataFrame(round(self.close - ((self.high - self.low) * 0.17), 2))
        self.df['s3'] = pd.DataFrame(round(self.close - ((self.high - self.low) * 0.27), 2))
        return self.df
