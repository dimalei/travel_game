class Timetable:
    def __init__(self, api: object) -> None:
        self.api = api

    def print_connections(self, station_name: str, amount=0) -> list:
        data = self.api.get_departure_info(station_name, amount)
        print(f"Connections from {data['stop']['name']}:")

        express_trains = {}
        for connection in data["connections"]:
            if connection['type'] == "express_train":
                express_trains[connection['line']] = connection['terminal']['name']
        if len(express_trains) == 0:
            print("Your location has no express tranis. You're fucked.")
            return None
        for connection in express_trains.items():
            print(connection)

if __name__ == "__main__":
    from search_api import SearchAPI
    search = SearchAPI()
    t = Timetable(search)
    t.print_connections("Aarau")