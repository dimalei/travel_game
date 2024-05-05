import urllib.parse
import urllib.request
import json


class SearchAPI:
    # handles the API stuff. Returns requestet values or None if something failed.
    # api found here

    def get_coordinates(stop_name: str) -> tuple:
        # returns the lattitute and longditude as a tuple
        url = "https://search.ch/timetable/api/station.json?"
        params = {"stop": stop_name}
        url = url + urllib.parse.urlencode(params)
        try:
            response = urllib.request.urlopen(url).read()
            data = json.loads(response)
            return (data["lat"], data["lon"])
        except TimeoutError("Connection timed out"):
            return None
        except KeyError(f"Station not found with {stop_name}"):
            return None

    def get_station_info(stop_name: str) -> tuple:
        # returns the lattitute and longditude as a tuple
        url = "https://search.ch/timetable/api/station.json?"
        params = {"stop": stop_name}
        url = url + urllib.parse.urlencode(params)
        try:
            response = urllib.request.urlopen(url).read()
            data = json.loads(response)
            if data["id"] != None:
                return data
            else:
                raise ValueError("Invalid Station Name.")
        except urllib.error.URLError:
            print("Connection timed out. Check your internet connection.")
            return None


if __name__ == "__main__":
    # print(SearchAPI.get_coordinates("Aarau"))
    print(SearchAPI.get_station_info("Aarau"))
