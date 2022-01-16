import unittest
import json
from datetime import timedelta
from pprint import pprint
import requests, requests_cache  # https://requests-cache.readthedocs.io/en/latest/
from duke_energy_outages import DukeEnergyOutages

requests_cache.install_cache('test_cache', backend='sqlite', expire_after=3600)

slong = requests_cache.CachedSession(expire_after=timedelta(hours=2))  # shared session, maintains cookies throughout
s = requests_cache.CachedSession(expire_after=timedelta(minutes=5))  # shared session, maintains cookies throughout

urls = [
    # 'https://outagemap.duke-energy.com/#/current-outages/ncsc',
    # 'https://outagemap.duke-energy.com/config/env.json',
    # 'https://outagemap.duke-energy.com/config/config.prod.json',
    # 'https://outagemap.duke-energy.com/assets/JSON/onboarding.json',
    'https://outagemap.duke-energy.com/assets/JSON/status-info.json',
    'https://outagemap.duke-energy.com/assets/county-coordinates/counties.NCSC.json',
    'https://outagemap.duke-energy.com/assets/jurisdiction-boundaries/boundaries.NCSC.json',
    'https://cust-api.duke-energy.com/outage-maps/v1/jurisdictions/DEC',
    'https://cust-api.duke-energy.com/outage-maps/v1/counties?jurisdiction=DEC',
    # 'https://cust-api.duke-energy.com/outage-maps/v1/alerts?jurisdiction=DEC',
    # 'https://cust-api.duke-energy.com/outage-maps/v1/outages?jurisdiction=DEP&swLat=33.842316&swLong=-84.321869&neLat=36.588117&neLong=-75.460621',
    # 'https://cust-api.duke-energy.com/outage-maps/v1/outages/outage?jurisdiction=DEP&sourceEventNumber=5449394'
]


class DukePowerOutageTest(unittest.TestCase):

    def test_state_level(self):
        uut = DukeEnergyOutages(short_expire_min=5)
        uut.get_state_summary(plot=False)

    def test_county_level(self):
        uut = DukeEnergyOutages()
        uut.get_county_summary()

    def test_outages(self):
        uut = DukeEnergyOutages()
        uut.get_individual_outages()

    def test_outage_details(self):
        uut = DukeEnergyOutages(short_expire_min=20)
        uut.outage_detail(5450188)


if __name__ == '__main__':
    unittest.main()
