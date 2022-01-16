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
        uut = DukeEnergyOutages()
        uut.get_state_level()


    def test_county_level(self):
        uut = DukeEnergyOutages()
        uut.get_state_level()


class MyTestCase(unittest.TestCase):

    def test_all(self):
        #NC bounding box -84.321869	33.842316	-75.460621	36.588117
        url = f"    'https://cust-api.duke-energy.com/outage-maps/v1/outages?jurisdiction=DEP&swLat=35.6&swLong=-78.8&neLat=35.7&neLong=-78.6',"
        for x in range (-754,-844, -1):
            lat=x/10.0
            print(lat)
            for y in range(338, 366, 1):
                lng = y / 10.0
                print(lng)

    def test_something(self):
        for url in urls:
            r = s.get(url, headers=headers)
            print(r.status_code, url)
            try:
                data = r.json()
                # pprint(data)
                if 'outage' in url:
                    print(len(data['data']))
                    print(json.dumps(data, indent=4))
                else:
                    print(json.dumps(data, indent=4)[:500])
            except:
                pass
        return

        url_map = 'https://outagemap.duke-energy.com/#/current-outages/ncsc'
        r = s.get(url_map)
        # url_county='https://outagemap.duke-energy.com/assets/county-coordinates/counties.NCSC.json'
        # r = s.get(url_county)
        # data = r.json()
        # pprint(data)
        url_count_alerts = 'https://cust-api.duke-energy.com/outage-maps/v1/counties?jurisdiction=DEC'
        r = s.get(url_count_alerts)
        data = r.json()
        pprint(data)


if __name__ == '__main__':
    unittest.main()
