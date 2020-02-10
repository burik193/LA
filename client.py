from requests import Session
from urllib import parse
import requests

# from warcraftlogs.models import Zone, Class
# from warcraftlogs.models.rankings import Fight


class WarcraftLogsClient:
    HOST = "https://www.warcraftlogs.com/v1/"

    def __init__(self, api_key):
        self.api_key = api_key
        self.session = Session()

    def _get(self, path, **kwargs):
        params = {"api_key": self.api_key}
        params.update(kwargs)

        url = parse.urljoin(self.HOST, path)

        return self.session.get(url, params=params)

    def zones(self):
        return self._get("zones").json()

    def classes(self):
        return self._get("classes").json()

    def rankings_encounter(self, encounter_id, **params):
        path = "rankings/encounter/{}".format(encounter_id)
        return self._get(path, **params).json()["rankings"]

    def report_fights(self, reportID):
        path = "https://www.warcraftlogs.com/v1/report/fights/{}?api_key={}".format(reportID, self.api_key)
        response = requests.get(path)
        return response.json()

    def report_player(self, player_name, serverName, serverRegion):
        path = "https://www.warcraftlogs.com/v1/parses/character/{}/{}/{}?api_key={}".format(player_name, serverName, serverRegion, self.api_key)
        response = requests.get(path)
        try:
            encoded = response.json()
        except:
            encoded = []
        return encoded

    def report_events(self, reportID, view='summary'):
        path = "https://www.warcraftlogs.com/v1/report/events/{}/{}?api_key={}".format(view, reportID, self.api_key)
        response = requests.get(path)
        return response.json()

    def report_guild_fights(self, guildName, serverName, serverRegion, **params):
        path = "/reports/guild/{}/{}/{}".format(guildName, serverName, serverRegion)
        return self._get(path, **params)

    def rankings_character(self, name, server, region, **params):
        path = "rankings/character/{}/{}/{}".format(name, server, region)
        return self._get(path, **params).json()