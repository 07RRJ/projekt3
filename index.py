from os import system
from threading import Thread
from time import sleep
from msvcrt import getwch

def Cls():
    system("cls")

class Elevator:
    DIRECTION = None
    FLOOR = 0
    STOPING_ON_FLOOR = False
    LIST_UP = []
    LIST_DOWN = []

    def CheckIfRequestToFloor(self):
        if self.FLOOR == 9:
            self.DIRECTION = "down"
            print("highest floor, going down")
            return
        elif self.FLOOR == 0:
            self.DIRECTION = "up"
            print("lowest floor, going up")
            return

        if self.DIRECTION == "up" and self.LIST_UP:
            return
        elif self.DIRECTION == "down" and self.LIST_DOWN:
            return
        else:
            self.DIRECTION = None
        
        if self.LIST_UP and self.DIRECTION == None:
            self.DIRECTION = "up"
        elif self.LIST_DOWN and self.DIRECTION == None:
            self.DIRECTION = "down"

    def Move(self):
        if self.DIRECTION == "up":
            self.FLOOR += 1
        if self.DIRECTION == "down":
            self.FLOOR -= 1

    def On(self):
        sleep(1)
        Cls()
        print(self.FLOOR, self.DIRECTION, self.FLOOR in self.LIST_UP, self.LIST_UP, self.FLOOR in self.LIST_DOWN, self.LIST_DOWN)
        self.CheckIfRequestToFloor()
        self.Move()
        if elevator.FLOOR in elevator.LIST_UP:
            print("you reached the floor")
            elevator.LIST_UP.remove(elevator.FLOOR)
        if elevator.FLOOR in elevator.LIST_DOWN:
            print("you reached the floor")
            elevator.LIST_DOWN.remove(elevator.FLOOR)
        print("enter on floor: ")
        self.On()

elevator = Elevator()

floors = [i for i in range(10)]

thread = Thread(target=elevator.On)

thread.start()

while True:
    
    try:
        floorRequest = int(getwch())
    except:
        pass
    if floorRequest != elevator.FLOOR and floorRequest in floors:
        if elevator.FLOOR < floorRequest and floorRequest not in elevator.LIST_UP:
            elevator.LIST_UP.append(floorRequest)
        elif elevator.FLOOR > floorRequest and floorRequest not in elevator.LIST_DOWN:
            elevator.LIST_DOWN.append(floorRequest)