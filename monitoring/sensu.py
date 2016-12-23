import json
import requests


class Pysensu():
    def __init__(self, host, user=None, password=None, port=4567, ssl=False):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.ssl = ssl
        self.api_url = self._build_api_url(host, user, password, port, ssl)

    def _build_api_url(self, host, user, password, port, ssl):
        protocol = 'http' if not ssl else 'https'

        credentials = ""
        if user and password:
            credentials = "{}:{}@".format(user, password)
        elif (user and not password) or (password and not user):
            raise ValueError("Must specify both user and password, or neither")

        return "{}://{}{}:{}".format(protocol, credentials, host, port)

    def get_all_events(self):
        r = requests.get("{}/events".format(self.api_url))
        if r.status_code != requests.codes.ok:
            raise ValueError("Error getting checks ({})".format(r.status_code))
        return r.json()
