from datetime import datetime
from save_json import list_to_json


class Timetable:
    def __init__(self, api: object) -> None:
        self.api = api

    def get_connections(self, station_name: str, time: datetime, amount=0) -> list:
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
        # list_to_json(data, "connection.json")
        my_connection = {}
        my_stops = []

        # get the connection with the selected line name
        for connection in data["connections"]:
            list_to_json(connection, "connection_test.json")
            for leg in connection["legs"]:
                # list_to_json(leg, "leg_test.json")
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


if __name__ == "__main__":
    from search_api import SearchAPI
    search = SearchAPI()
    t = Timetable(search)
    time = datetime.now()
    # t.get_connections("Aarau", time)
    print(t.get_stops("IR 35", "Aarau", "Basel", time))