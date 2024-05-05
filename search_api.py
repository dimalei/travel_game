import urllib.parse
import urllib.request
import json


class SearchAPI:
    # handles the API stuff. Returns requestet values or None if something failed.
    # api found here
    def __init__(self) -> None:
        self.station_queries = 0
        self.timetable_queries = 0

    def get_station_info(self, stop_name: str) -> tuple:
        # returns station info as json
        url = "https://search.ch/timetable/api/station.json?"
        params = {"stop": stop_name}
        url = url + urllib.parse.urlencode(params)
        try:
            response = urllib.request.urlopen(url).read()
            self.station_queries += 1
            data = json.loads(response)
            if data["id"] != None:
                return data
            else:
                raise ValueError("Invalid Station Name: {self.stop_name}")
        except urllib.error.URLError:
            print("Connection timed out. Check your internet connection.")
            return None

    def get_departure_info(self, stop_name: str) -> tuple:
        # returns available connections from stop name a json
        url = "https://search.ch/timetable/api/stationboard.json?"
        params = {"stop": stop_name, "transportation_types":"train"}
        url = url + urllib.parse.urlencode(params)
        try:
            response = urllib.request.urlopen(url).read()
            self.timetable_queries += 1
            data = json.loads(response)
            if data["stop"]["id"] != None:
                return data
            else:
                raise ValueError("Invalid Station Name: {self.stop_name}")
        except urllib.error.URLError:
            print("Connection timed out. Check your internet connection.")
            return None

if __name__ == "__main__":
    a = SearchAPI()
    # print(SearchAPI.get_coordinates("Aarau"))
    # print(SearchAPI.get_station_info("Aarau"))
    print(a.get_departure_info("Aarau"))
