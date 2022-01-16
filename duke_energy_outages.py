import unittest
import json
from datetime import timedelta
import pandas  as pd
from pprint import pprint
import requests, requests_cache  # https://requests-cache.readthedocs.io/en/latest/

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 900)


class DukeEnergyOutages():

    def __init__(self, short_expire_min=5, long_expire_hours=1):
        self.s = requests_cache.CachedSession(expire_after=timedelta(minutes=short_expire_min))
        self.s_long = requests_cache.CachedSession(expire_after=timedelta(hours=long_expire_hours))
        self.url_base = 'https://cust-api.duke-energy.com'
        self.url_api_base = 'https://cust-api.duke-energy.com/outage-maps/v1/'
        self.headers = {'Authorization': 'Basic RENzalVVNzF5dlRNeEFnZHZMRXJVUkxLcHNlOHBqR3g6YjJMb0R3c01TbXBFMFpySw=='}

    def __del__(self):
        self.s.close()

    def get_state_level(self):
        filename = 'duke_state.csv'
        try:
            df_cache = pd.read_csv(filename)
            df_cache.index = df_cache['lastUpdated']
            cache=df_cache.to_dict('index')
        except:
            df_cache = pd.DataFrame()
            cache={}
        url = f'{self.url_api_base}/jurisdictions/DEC'
        r = self.s.get(url, headers=self.headers)
        try:
            data = r.json()
        except:
            data = {}
        if 'data' in data.keys():
            data['data']['customersAffectedNC'] = data['data']['customersAffectedPerState']['NC']
            data['data']['customersAffectedSC'] = data['data']['customersAffectedPerState']['SC']
            del (data['data']['customersAffectedPerState'])
            del (data['data']['stateDescription'])
            cache[data['data']['lastUpdated']]=data['data']
            df = pd.DataFrame.from_dict(cache, orient='index', columns=data['data'].keys())
            df.index = df['lastUpdated']
            df.to_csv(filename)


    def get_state_level(self):
        filename = 'duke_state.csv'
        try:
            df_cache = pd.read_csv(filename)
            df_cache.index = df_cache['lastUpdated']
            cache=df_cache.to_dict('index')
        except:
            df_cache = pd.DataFrame()
            cache={}
        url = f'{self.url_api_base}/jurisdictions/DEC'
        r = self.s.get(url, headers=self.headers)
        try:
            data = r.json()
        except:
            data = {}
        if 'data' in data.keys():
            data['data']['customersAffectedNC'] = data['data']['customersAffectedPerState']['NC']
            data['data']['customersAffectedSC'] = data['data']['customersAffectedPerState']['SC']
            del (data['data']['customersAffectedPerState'])
            del (data['data']['stateDescription'])
            cache[data['data']['lastUpdated']]=data['data']
            df = pd.DataFrame.from_dict(cache, orient='index', columns=data['data'].keys())
            df.index = df['lastUpdated']
            df.to_csv(filename)
