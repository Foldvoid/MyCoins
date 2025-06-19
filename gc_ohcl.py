from pycoingecko import CoinGeckoAPI
import pandas as pd
import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView
from PyQt5.QtCore import Qt, QAbstractTableModel


import json_manager


class CrytoCoin():
    def __init__(self):
        print('loop')
        self.id, self.currency = 'bitcoin', 'usd'
        self.cg = CoinGeckoAPI()

        file_name = self.id + '.json'
        self.ohlc_file_path = './api_data/ohlc_' + file_name
        self.ohlc = None
        self.set_data_frame()

    def set_id(self, id):
        self.id = id

    def set_currency(self, currency):
        self.currency = currency

    def set_data_frame(self):
        if os.path.exists(self.ohlc_file_path):
            self.ohlc = json_manager.read_json(self.ohlc_file_path)
        else:
            self.ohlc = self.cg.get_coin_ohlc_by_id(id=self.id, vs_currency=self.currency, days='30')
            json_manager.write_json(self.ohlc_file_path, self.ohlc)

    def get_data_frame(self):
        df = pd.DataFrame(self.ohlc)
        df.columns = ['date', 'open', 'high', 'low', 'close']
        df['date'] = pd.to_datetime(df['date'], unit='ms')
        df.set_index('date', inplace=True)
        return df

    def refresh(self):
        file_name = self.id + '.json'
        self.ohlc_file_path = './api_data/ohlc_' + file_name

        self.set_data_frame()


cr_coin = CrytoCoin()
