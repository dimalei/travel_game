from location import Location
from search_api import SearchAPI
from timetable import Timetable
from clock import Clock
import person


class Game:
    def __init__(self) -> None:
        search_api = SearchAPI()
        self.tt = Timetable(search_api)
        self.mrx = person.Target(search_api)
        while True:
            location_input = input("Enter your starting location:\n")
            try:
                self.player = person.Player(
                    Location(location_input, search_api))
                break
            except ValueError:
                print("Invalid Location Name. Try again.")
        self.clock = Clock()

    def help(self):
        print("[1] take a train [2] exit")

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
                # taking a train
                if self.take_train() == None:
                    break
                # print("work in progress")
            elif command == "2":
                break
            else:
                self.help()
        print("######## GAME OVER ########")

    def take_train(self):
        # choose connection
        connection = self.choose_connection()
        if connection == None: return   # acton cancelled



    def choose_connection(self) -> tuple:
        # get a list of connections, choose a line, choose how many stations and then move the player
        connections = self.tt.get_connections(
            self.player.location.name, self.clock + self.player.time_travelled)
        line = ""
        terminal = ""
        print("Select your Connection:")
        for i, connection in enumerate(connections.items()):
            print(
                f"[{i+1}] {connection[0]:<5} to {connection[1]['destination']:<16} at {connection[1]['departure'][11:16]}")
        print("[0] Cancel")
        while True:
            line = input()
            try:
                line = int(line)
            except ValueError:
                print("Enter a number.")
                continue
            if line - 1 in range(len(connections)):
                # line selected
                for i, connection in enumerate(connections.items()):
                    if i + 1 == line:
                        line = connection[0]
                        terminal = connection[1]['destination']
                        break
                break
            elif line == 0:
                # cancel taking the train
                return None
            else:
                print("Invalid Input")
        # print(f"selected line: {line}, terminal: {terminal}")
        return (line, terminal)


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
        print("[1] start new game, [2] exit")

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
