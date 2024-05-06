from location import Location
from search_api import SearchAPI
from timetable import Timetable
from clock import Clock
import person
from datetime import datetime

from save_json import list_to_json


class Game:
    def __init__(self) -> None:
        self.search_api = SearchAPI()
        self.tt = Timetable(self.search_api)
        self.mrx = person.Target(self.search_api)
        while True:
            location_input = input("Enter your starting location:\n")
            try:
                self.player = person.Player(
                    Location(location_input, self.search_api))
                break
            except ValueError:
                print("Invalid Location Name. Try again.")
        self.start_time = datetime.now()
        self.turns = 1

    def help(self):
        print("[1] take a train [2] go to place [3] exit")

    def print_status(self):
        print(f"You are now in {self.player.location.name}. Now is {(self.start_time+self.player.time_travelled).strftime('%A, %H:%M')}")
        print(
            f"Your target is {self.player.distance_to_person(self.mrx)} km from your position.")

    def loop(self):
        while True:
            print(f"{'#'*20} Turn {self.turns:02} {'#'*20}")
            self.print_status()
            while True:
                self.help()
                command = input("Command:\n").strip()
                if command == "1":
                    # taking a train
                    if self.take_train():
                        self.turns += 1
                        break
                    # print("work in progress")
                elif command == "2":
                    # direct connection
                    break
                elif command == "3":
                    return
                else:
                    self.help()

    def take_train(self):
        # choose connection
        connection = self.choose_connection()
        if connection == None: return   # action cancelled

        # choose station to travel to
        station = self.choose_stop(connection[0], connection[1])
        if station == None: return     # action cancelled

        # arrival time is YYYY DD MM (wtf)
        time_passed = datetime.strptime(station["arrival"], "%Y-%d-%m %H:%M:%S") - self.start_time
        print(time_passed)
        self.player.move(Location(station["stop"], self.search_api), time_passed)
        return True


    def choose_stop(self, line: str, terminal: str) -> dict:
        print(f"line {line} terminal {terminal}")
        stops = self.tt.get_stops(line, self.player.location.name, terminal, self.start_time + self.player.time_travelled)
        print("Select your Stop:")
        for i, stop in enumerate(stops):
            print(f"[{i+1}] {stop['stop']} {stop['arrival'][11:16]}, ", end="")
        print("[0] Cancel")
        while True:
            stop_selction = input()
            try:
                stop_selction = int(stop_selction)
            except ValueError:
                print("Enter a number.")
                continue
            if stop_selction - 1 in range(len(stops)):
                return stops[stop_selction - 1]
            elif stop_selction == 0:
                return None
            else:
                print("Invalid Input")



    def choose_connection(self) -> tuple:
        # returns the line and the terminal station that the player selected: (line, terminal) eg. (IR 16, Zürich HB)
        connections = self.tt.get_connections(
            self.player.location.name, self.start_time + self.player.time_travelled)
        line_selection = ""
        terminal = ""
        print("Select your Connection:")
        for i, connection in enumerate(connections.items()):
            print(
                f"[{i+1}] {connection[0]:<5} to {connection[1]['destination']:<16} at {connection[1]['departure'][11:16]}")
        print("[0] Cancel")
        while True:
            line_selection = input()
            try:
                line_selection = int(line_selection)
            except ValueError:
                print("Enter a number.")
                continue
            if line_selection - 1 in range(len(connections)):
                # line selected
                for i, connection in enumerate(connections.items()):
                    if i + 1 == line_selection:
                        line_selection = connection[0]
                        terminal = connection[1]['destination']
                        break
                break
            elif line_selection == 0:
                # cancel taking the train
                return None
            else:
                print("Invalid Input")
        # print(f"selected line: {line}, terminal: {terminal}")
        return (line_selection, terminal)


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
        print("######## GAME OVER ########")

if __name__ == "__main__":
    a = Application()
    a.execute()
