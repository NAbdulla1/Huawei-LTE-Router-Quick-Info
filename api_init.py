from huawei_lte_api.Client import Client
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
from huawei_lte_api.Connection import Connection


class ApiInitializer:
    def __init__(self, url):
        self.client = None
        self.getClient()
        self.url = url

    def loggedIn(self):
        try:
            self.client.device.information()
        except:
            return False
        return True

    def getNewClient(self):
        try:
            connection = AuthorizedConnection(self.url, timeout=2)
            self.client = Client(connection)
        except:
            self.client = None

    def getClient(self):
        if self.client is None or not self.loggedIn():
            self.getNewClient()
        return self.client
