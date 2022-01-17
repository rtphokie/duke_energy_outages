import unittest
import time
import json
from datetime import timedelta
from pprint import pprint
import requests, requests_cache  # https://requests-cache.readthedocs.io/en/latest/
from duke_energy_outages import DukeEnergyOutages

requests_cache.install_cache('test_cache', backend='sqlite', expire_after=3600)

slong = requests_cache.CachedSession(expire_after=timedelta(hours=2))  # shared session, maintains cookies throughout
s = requests_cache.CachedSession(expire_after=timedelta(minutes=5))  # shared session, maintains cookies throughout


class DukePowerOutageTest(unittest.TestCase):

    def test_0_state_level(self):
        uut = DukeEnergyOutages(short_expire_min=10)
        uut.get_state_summary(plot=True)

    def test_1_county_level(self):
        uut = DukeEnergyOutages()
        uut.get_county_summary()

    def test_2_outages(self):
        uut = DukeEnergyOutages()
        uut.get_individual_outages()

if __name__ == '__main__':
    while(True):
        uut = DukeEnergyOutages(short_expire_min=10)
        uut.get_state_summary(plot=False)
        uut.get_county_summary()
        uut.get_individual_outages()
        time.sleep(10*60)
