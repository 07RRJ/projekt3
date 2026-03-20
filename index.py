from os import system

def Cls():
    system("cls")

class Elevator:
    DIRECTION = "up"
    FLOOR = 0
    STOPING_ON_FLOOR = False

    def CheckIfRequestToFloor(self, listUp, listDown):
        if self.FLOOR == 9:
            self.DIRECTION = "down"
            print("highest floor, going down")
            return
        elif self.FLOOR == 0:
            self.DIRECTION = "up"
            print("lowest floor, going up")
            return

        if self.DIRECTION == "up" and listUp:
            return
        elif self.DIRECTION == "down" and listDown:
            return
        else:
            self.DIRECTION = None
        
        if listUp and self.DIRECTION == None:
            self.DIRECTION = "up"
        elif listDown and self.DIRECTION == None:
            self.DIRECTION = "down"

    def Move(self):
        if self.DIRECTION == "up":
            self.FLOOR += 1
        if self.DIRECTION == "down":
            elevator.FLOOR -= 1

elevator = Elevator()

listUp = []
listDown = []

floors = [i for i in range(10)]

while True:
    print(elevator.FLOOR, elevator.DIRECTION, elevator.FLOOR in listUp, listUp, elevator.FLOOR in listDown, listDown)
    if elevator.FLOOR in listUp:
        print("you reached the floor")
        listUp.remove(elevator.FLOOR)
    if elevator.FLOOR in listDown:
        print("you reached the floor")
        listDown.remove(elevator.FLOOR)
    elevator.CheckIfRequestToFloor(listUp, listDown)
    try:
        floorRequest = int(input("enter on floor: "))
    except:
        pass
    Cls()
    if floorRequest != elevator.FLOOR and floorRequest in floors:
        if elevator.FLOOR < floorRequest and floorRequest not in listUp:
            listUp.append(floorRequest)
        elif elevator.FLOOR > floorRequest and floorRequest not in listDown:
            listDown.append(floorRequest)
    elevator.Move()