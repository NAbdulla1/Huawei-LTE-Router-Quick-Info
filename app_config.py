import os.path
import json

import util


class AppConfig:
    def __init__(self):
        self.conf_file = 'conf.json'
        self.default_conf = """
                            {
                                "router-ip": "192.168.8.1",
                                "admin": {
                                    "username": "admin",
                                    "password": "qwerty5"
                                },
                                "update-interval": 1,
                                "color1": {
                                    "r": 250,
                                    "g": 250,
                                    "b": 250
                                },
                                "color2": {
                                    "r": 220,
                                    "g": 0,
                                    "b": 220
                                }
                            }
                            """
        self.config = self._readConf()

    def getUrl(self):
        username = self.config["admin"]["username"]
        password = self.config['admin']['password']
        router_ip = self.config['router-ip']
        return f'http://{username}:{password}@{router_ip}'

    def getUpdateInterval(self):
        return self.config['update-interval']

    def getColor(self, colorNum: int):
        color = self.config['color1']
        if colorNum == 2:
            color = self.config['color2']
        return util.from_rgb(color['r'], color['g'], color['b'])

    def _readConf(self):
        self._createIfNotExists()
        with open('conf.json', 'r') as conf:
            return json.load(conf)

    def _createIfNotExists(self):
        if not os.path.exists(self.conf_file):
            print("creating '{self.conf_file}' file")
            tmp = open(self.conf_file, 'w+')
            tmp.write(self.default_conf)
            tmp.flush()
            tmp.close()
