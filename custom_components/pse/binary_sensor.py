import csv
import datetime
import requests

from homeassistant.components.binary_sensor import BinarySensorEntity


def setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([PSEBinarySensor()], True)


class PSEBinarySensor(BinarySensorEntity):
    def __init__(self):
        self.data = None

    @property
    def name(self):
        return "PSE peak hour"

    @property
    def is_on(self):
        if self.data is None:
            return None
        return not self.data[3].startswith("NORMALNE")

    @property
    def extra_state_attributes(self):
        output = dict()
        if self.data is not None:
            output["demand"] = float(self.data[3].replace(",","."))
        return output

    @property
    def icon(self):
        if self.is_on:
            return 'mdi:transmission-tower-off'
        return 'mdi:transmission-tower'

    def update(self):
        now = datetime.datetime.now()
        now_hour = now.strftime("%-H")
        response = requests.get(f"https://www.pse.pl/getcsv/-/export/csv/PL_GS/data/{now.strftime('%Y%m%d')}")
        csv_output = csv.reader(response.text.splitlines(), delimiter=";")
        self.data = next(filter(lambda r: r[1] == now_hour, csv_output))
        