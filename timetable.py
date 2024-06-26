from datetime import datetime
from save_json import list_to_json


class Timetable:
    def __init__(self, api: object) -> None:
        self.api = api

    def get_departures(self, station_name: str, time: datetime, amount=0) -> list:
        # gets a complete list of departures and returns a filtered list of the next high speed connections
        data = self.api.get_departure_info(station_name, amount, time.strftime("%H:%M"), time.strftime("%d/%m/%Y"))
        express_trains = {}
        for connection in data["connections"]:
            if connection['type'] == "express_train" and connection['line'] not in express_trains:
                express_trains[connection['line']] = {"destination":connection['terminal']['name'], "departure":connection['time']}
        if len(express_trains) == 0:
            print("Your location has no express tranis. You're fucked.")
            return None
        return express_trains

    def get_stops(self,line: str, origin: str, destination: str, time: datetime, amount=20):
        # retuns a list of stops on the selected line [(stop_name, arrival_time),(stop_name, arrival_time), etc.]
        data = self.api.get_route(origin, destination, time.strftime("%H:%M"), time.strftime("%d/%m/%Y"), amount)
        my_connection = {}
        my_stops = []

        # get the connection with the selected line name
        for connection in data["connections"]:
            for leg in connection["legs"]:
                if "line" in leg:
                    if line == leg["line"]:
                        my_connection = connection
                        break
            if my_connection != {}:
                break
        # take the first one available if no line exists
        if my_connection == {}:
            my_connection = data["connections"][0]

        # create the list with the stops withn that connection
        for leg in my_connection["legs"]:
            if "stops" in leg:
                if isinstance(leg["stops"], list):
                    for stop in leg["stops"]:
                        if "arrival" in stop:
                            my_stops.append({"stop":stop['name'], "arrival":stop['arrival']})
            if "exit" in leg:
                my_stops.append({"stop":leg["exit"]["name"], "arrival":leg["exit"]["arrival"]})
        
        return my_stops

    def get_direct(self, origin: str, destination: str, time: datetime) -> dict:
        # returns a dict with the destination and arrival time of the desired destination (stop_name, arrival_time)
        data = self.api.get_route(origin, destination, time.strftime("%H:%M"), time.strftime("%d/%m/%Y"), num=1)
        if "connections" in data:
            return {"stop":data["connections"][0]["to"], "arrival":data["connections"][0]["arrival"]}

    def stops_to(self, player_location: str, target_location, time: datetime) -> int:
        data = self.api.get_route(player_location, target_location, time.strftime("%H:%M"), time.strftime("%d/%m/%Y"), num=1)
        stops = 0
        for leg in data["connections"][0]["legs"]:
            if leg["stops"] != None:
                stops += len(leg["stops"])
            else:
                stops += 1
        return stops


if __name__ == "__main__":
    from search_api import SearchAPI
    search = SearchAPI()
    t = Timetable(search)
    time = datetime.now()
    # t.get_connections("Aarau", time)
    # print(t.get_stops("IR 35", "Aarau", "Basel", time))
    print(t.stops_to("Aarau", "Basel", time))