import unittest
import json
from datetime import timedelta
import pandas  as pd
from pprint import pprint
import requests, requests_cache  # https://requests-cache.readthedocs.io/en/latest/
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 900)


class DukeEnergyOutages():

    def __init__(self, short_expire_min=5, long_expire_hours=1, jurisdiction='DEC'):
        self.s = requests_cache.CachedSession(expire_after=timedelta(minutes=short_expire_min))
        self.s_long = requests_cache.CachedSession(expire_after=timedelta(hours=long_expire_hours))
        self.s_no_cache = requests_cache.CachedSession(expire_after=timedelta(seconds=15))
        self.url_base = 'https://cust-api.duke-energy.com'
        self.url_api_base = 'https://cust-api.duke-energy.com/outage-maps/v1/'
        self.headers = {'Authorization': 'Basic RENzalVVNzF5dlRNeEFnZHZMRXJVUkxLcHNlOHBqR3g6YjJMb0R3c01TbXBFMFpySw=='}
        self.jurisdiction=jurisdiction

    def __del__(self):
        self.s.close()

    def get_state_level(self):
        '''
        top level data, use 15 second cache to ease impact of repeated unit testing
        :return:
        '''
        filename = 'duke_state.csv'
        try:
            df_cache = pd.read_csv(filename)
            df_cache.index = df_cache['lastUpdated']
            cache = df_cache.to_dict('index')
        except:
            df_cache = pd.DataFrame()
            cache = {}
        url = f'{self.url_api_base}/jurisdictions/{self.jurisdiction}'
        r = self.s_no_cache.get(url, headers=self.headers)
        try:
            data = r.json()
        except:
            data = {}
        if 'data' in data.keys():
            data['data']['customersAffectedNC'] = data['data']['customersAffectedPerState']['NC']
            data['data']['customersAffectedSC'] = data['data']['customersAffectedPerState']['SC']
            del (data['data']['customersAffectedPerState'])
            del (data['data']['stateDescription'])
            cache[data['data']['lastUpdated']] = data['data']
            df = pd.DataFrame.from_dict(cache, orient='index', columns=data['data'].keys())
            df.index = df['lastUpdated']
            df.to_csv(filename)
        df2=df[['customersAffectedNC', 'customersAffectedSC','lastUpdated']]
        # df2.index = df2['lastUpdated']
        df2.rename(columns={"customersAffectedNC": "NC", "customersAffectedSC": "SC"}, inplace=True)
        lines = df2.plot.line()
        plt.show()

    def get_county_level(self):
        filename = 'duke_county.csv'
        try:
            df_cache = pd.read_csv(filename)
            df_cache.index = df_cache['areaOfInterestName-lastUpdated']
            cache = df_cache.to_dict('index')
        except:
            df_cache = pd.DataFrame()
            cache = {}
        url = f'{self.url_api_base}/counties?jurisdiction={self.jurisdiction}'
        r = self.s.get(url, headers=self.headers)
        try:
            data = r.json()
        except:
            data = {}
        if 'data' in data.keys():
            print(r.from_cache)
            records={}
            for record in data['data']:
                if 'areaOfInterestSummary' in record.keys():
                    for p, v in record['areaOfInterestSummary'].items():
                        record[p]=v
                    # del(record['areaOfInterestSummary'])
                for column in ['serviceAreas', 'areaOfInterestSummary','jurisdiction']:
                    del (record[column])
                record['areaOfInterestName-lastUpdated']=f"{record['areaOfInterestName']}-{record['lastUpdated']}"
                records[record['areaOfInterestName-lastUpdated']]=record
            df = pd.DataFrame.from_dict(records, orient='index', columns=record.keys())
            df.index = df['areaOfInterestName-lastUpdated']
            df.to_csv(filename)
