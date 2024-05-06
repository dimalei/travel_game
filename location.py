import math


class Location:
    # defines a location based on a train station
    def __init__(self, name: str, api) -> None:
        self.api = api
        station_info = api.get_station_info(name)
        if station_info == None:
            raise ConnectionError(
                "Could not veryfy loctation from the internet.")
        self.name = station_info["name"]
        self.coordinates = (station_info["lat"], station_info["lon"])

    def distance_to(self, another: "Location") -> int:
        # returns the distance to another location in km
        # formula https://community.fabric.microsoft.com/t5/Desktop/How-to-calculate-lat-long-distance/td-p/1488227
        distance = math.acos(math.sin(math.radians(self.coordinates[0]))*math.sin(math.radians(another.coordinates[0]))+math.cos(math.radians(
            self.coordinates[0]))*math.cos(math.radians(another.coordinates[0]))*math.cos(math.radians(another.coordinates[1]-self.coordinates[1])))*6371
        return int(distance)

    def NSWE_to(self, another: "Location") -> str:
        # returns direction
        # source https://stackoverflow.com/questions/47659249/calculate-cardinal-direction-from-gps-coordinates-in-python
        points = ["north", "north east", "east", "south east",
                  "south", "south west", "west", "north west"]
        bearing = self.calcBearing(self.coordinates[0], self.coordinates[1], another.coordinates[0], another.coordinates[1])
        bearing += 22.5
        bearing = bearing % 360
        bearing = int(bearing / 45)  # values 0 to 7
        NSEW = points[bearing]
        return NSEW

    def calcBearing(self, lat1, long1, lat2, long2):
        dLon = (long2 - long1)
        x = math.cos(math.radians(lat2)) * math.sin(math.radians(dLon))
        y = math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - math.sin(
            math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(math.radians(dLon))
        bearing = math.atan2(x, y)   # use atan2 to determine the quadrant
        bearing = math.degrees(bearing)
        return bearing

    def __str__(self) -> str:
        return f"{self.name}, {self.coordinates}"


if __name__ == "__main__":
    from search_api import SearchAPI
    api = SearchAPI()
    a = Location("Aarau", api)
    # b = Location("jhgh") # raises ValueError
    b = Location("Bern", api)
    print(a)
    print(f"distance form {a.name} to {b.name} is {a.distance_to(b)}km")
    print(f"directoion form {a.name} to {b.name} is {a.NSWE_to(b)}")
