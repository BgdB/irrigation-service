import configparser
import json
from gpiozero import OutputDevice

config = configparser.ConfigParser()

config.read('config.ini')
ACTIVE_ZONES = json.loads(config['DEFAULT']['zones'])
USER = config['DEFAULT']['user']
DEVICES = {}

for zone_id in ACTIVE_ZONES:
    DEVICES[zone_id] = OutputDevice(int(zone_id))
