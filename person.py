from location import Location
import json
from random import choice
from datetime import timedelta


class Person:
    def __init__(self, location: Location) -> None:
        self.location = location
        self.time_travelled = timedelta()

    def move(self, new_location: Location, time_passed: timedelta):
        self.location = new_location
        self.time_travelled = time_passed

    def __str__(self) -> str:
        return f"Location: {self.location}, travelled: {self.time_travelled}"

    def distance_to_person(self, another: "Person") -> int:
        return self.location.distance_to(another.location)

class Target(Person):
    # The starting position of the target person is randomly picked from a list
    def __init__(self, api) -> None:
        super().__init__(Location(self.random_location(), api))

    def random_location(self) -> str:
        locations = {}
        with open("start_locations.json") as my_locations:
            data = my_locations.read()
            locations = json.loads(data)
        random_loc = choice(locations["starting_locations"])
        return random_loc


class Player(Person):
    def __init__(self, location: Location) -> None:
        super().__init__(location)


if __name__ == "__main__":
    mrx = Target()
    # player = Player(Location("asdf")) # raises value error
    player = Player(Location("Aarau"))

    print(mrx)
    print(player)
