from datetime import datetime

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

    def get_line(self,line: str, origin: str, destination: str, time: datetime, amount=20):
        data = self.api.get_route(origin, destination, time.strftime("%H:%M"), time.strftime("%d/%m/%Y"), amount)
        stops = []
        my_connection = {}
        for connection in data["connections"]:
            print(connection["legs"][0]["line"])
            if connection["legs"][0]["line"] == line:
                my_connection = connection
                break
        print(my_connection)
        return my_connection


if __name__ == "__main__":
    from search_api import SearchAPI
    search = SearchAPI()
    t = Timetable(search)
    time = datetime.now()
    # t.get_connections("Aarau", time)
    t.get_line("IR 16", "Aarau", "Zürich", time)