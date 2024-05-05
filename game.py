from location import Location
import person

class Game:
    def __init__(self) -> None:
        self.mrx = person.Target()
        while True:
            location_input = input("Enter your starting location:\n")
            try:
                self.player = person.Player(Location(location_input))
                break
            except ValueError:
                print("Invalid Location Name. Try again.")

    def execute(self):
        print(f"you are {self.player.location.distance_to(self.mrx.location)} km from your target")
        pass



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
        self.help()
        while True:
            command = input("Command:\n")
            if command == "1":
                session = Game()
                session.execute()
            elif command == "2":
                break
            else:
                self.help()

a = Application()
a.execute()
    
