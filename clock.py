from datetime import datetime
from datetime import timedelta

class Clock:
    def __init__(self) -> None:
        self.__start = datetime.now()

    def now(self, offset: timedelta):
        return (self.__start + offset).strftime("%H:%M")

    def __add__(self, other):
        return self.__start + other

if __name__ == "__main__":
    c = Clock()
    delta = timedelta(hours=1, minutes=3)
    print(c.now(delta))