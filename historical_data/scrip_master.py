import pandas as pd

# pandas set options for full length view
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


class ScripMaster:
    def __init__(self, scrip_master_url: str):
        self.symbol_data = None
        self.scrip_master_url = scrip_master_url
        self.df = pd.read_csv(self.scrip_master_url)

    def scrip_code(self, symbol, exch_type, cp_type, exch=None):
        if exch_type == 'C':
            self.symbol_data = self.df.loc[
                (self.df['Root'] == symbol.upper()) & (self.df['ExchType'] == exch_type.upper()) & (self.df['Exch'] == exch.upper())]
        else:
            self.symbol_data = self.df.loc[(self.df['Root'] == symbol.upper()) & (self.df['ExchType'] == exch_type) & (
                    self.df['CpType'] == cp_type)]
        return self


    # def get_expiry(self, code=253345):
    #     df = self.scrip_code().df
    #     # self.df = df.loc[(df['Scripcode'] == code)]
    #     self.df = df.loc[(df['name'] == "NIFTY")]
    #     # self.expiry_dates_obj = self.client.get_expiry("N", symbol=symbol.upper())
    #     # self.rounded_ltp = self.rounded_LTP(self.expiry_dates_obj).rounded_ltp
    #     # self.expiry_dates = self.expiry_dates_obj.get('Expiry')
    #     # self.expiry = self.expiry_dates[index].get('ExpiryDate')
    #     # self.expiry_int = self.timestamp_to_int(self.expiry)
    #     return self


scrip_csv_url = "https://images.5paisa.com/website/scripmaster-csv-format.csv"
scriper = ScripMaster(scrip_csv_url)
data = {
    "symbol": 'reliance', "exch_type": 'D', "cp_type": 'XX', 'exch': 'N'
}
# print(scriper.scrip_code(**data).symbol_data)
