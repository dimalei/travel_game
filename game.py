from location import Location
from search_api import SearchAPI
from timetable import Timetable
import person


class Game:
    def __init__(self) -> None:
        search_api = SearchAPI()
        self.mrx = person.Target(search_api)
        while True:
            location_input = input("Enter your starting location:\n")
            try:
                self.player = person.Player(Location(location_input, search_api))
                break
            except ValueError:
                print("Invalid Location Name. Try again.")
        self.timetable = Timetable(search_api)

    def help(self):
        print("move to: 1 | exit: 2")

    def print_distance_target(self):
        print(
            f"you are {self.player.distance_to_person(self.mrx)} km from your target")

    def loop(self):
        print("###########")
        self.print_distance_target()
        while True:
            self.help()
            command = input("Command:\n").strip()
            if command == "1":
                # move
                if self.timetable.print_connections(self.player.location.name) == None:
                    break
                # print("work in progress")
            elif command == "2":
                break
            else:
                self.help()
        print("######## GAME OVER ########")


class Application:
    version = "0.0.1"

    def __init__(self) -> None:
        pass

    def welcome(self):
        with open("art.txt") as art:
            word_art = art.read()
            print(word_art)
            print(f"{'Version: ' + self.version:^88}")

    def help(self):
        print("start new game: 1 | exit: 2")

    def execute(self):
        self.welcome()
        while True:
            self.help()
            command = input("Command:\n")
            if command == "1":
                session = Game()
                session.loop()
            elif command == "2":
                break
            else:
                self.help()


if __name__ == "__main__":
    a = Application()
    a.execute()
