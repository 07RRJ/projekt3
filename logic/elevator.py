import pygame
from ui.elements import Text
from threading import Thread, Lock

BASE_WIDTH, BASE_HEIGHT = 2000, 1130
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
clock = pygame.time.Clock()

floors = {i:i*110+20 for i in range(10)}
dirrectionKeys = {i: ("up" if i%2 else "down", 9-(i-9)//2) for i in range(10, 28)}

class Elevator:
    _lock = Lock()
    DIRECTION: bool = None
    MOVING: bool = False
    GOING = Text("On floor: 1")
    FLOOR: int = 0
    STOPING_ON_FLOOR: bool = False
    LIST_UP: list = []
    LIST_DOWN: list = []
    elevator_shaft = None

    def __init__(self):
        self.x: int = BASE_WIDTH//2-40
        self.y: int = BASE_HEIGHT-120
        self.rect: pygame.rect = pygame.Rect(self.x, self.y, 80, 100)

    def AddFloor(self, floor):
        if floor in floors.keys(): # floor 1-10 with keypad (0-9)
            if self.FLOOR < floor and floor not in self.LIST_UP:
                self.LIST_UP.append(floor)
            elif self.FLOOR > floor and floor not in self.LIST_DOWN:
                self.LIST_DOWN.append(floor)
            else:
                return

        elif floor in dirrectionKeys.keys(): # up/down buttons outside self (10-27). even = down (10, 12, 14). odd = up (11, 13, 15)
            print(dirrectionKeys[floor])
            selectedDir = dirrectionKeys[floor][0]
            selectedFloor = dirrectionKeys[floor][1]
            if selectedDir == "up" and selectedFloor not in self.LIST_UP:
                self.LIST_UP.append(selectedFloor)
            elif selectedDir == "down" and selectedFloor not in self.LIST_DOWN:
                self.LIST_DOWN.append(selectedFloor)
            else:
                return

        self.TellDirrection()
        with self._lock:
            if self.MOVING == False:
                Thread(target=self.On, daemon=True).start()
                self.MOVING = True

    def CheckIfRequestToFloor(self):
        if self.DIRECTION == "up" and self.LIST_UP:
            return
        elif self.DIRECTION == "down" and self.LIST_DOWN:
            return
        else:
            self.DIRECTION = None
        
        if self.LIST_UP and self.DIRECTION == None:
            try:
                if min(self.LIST_UP) > self.FLOOR:
                    self.DIRECTION = "up"
                else:
                    self.DIRECTION = "down"
            except:
                pass
        elif self.LIST_DOWN and self.DIRECTION == None:
            try:
                if max(self.LIST_UP) < self.FLOOR:
                    self.DIRECTION = "down"
                else:
                    self.DIRECTION = "up"
            except:
                pass

    def TellDirrection(self):
        text = ""
        if self.DIRECTION == "up":
            text = f"Moving up to floor: {min(self.LIST_UP)+1}"
        elif self.DIRECTION == "down":
            text = f"Moving down to floor: {max(self.LIST_DOWN)+1}"
        else:
            text = f"On floor: {self.FLOOR+1}"
        self.GOING = Text(text)

    def Move(self):
        if self.DIRECTION == "up":
            if self.FLOOR < 9:
                self.FLOOR += 1
                for i in range(110):
                    clock.tick(200)
                    self.y -= 1
                    self.rect = pygame.Rect(self.x, self.y, 80, 100)
            else:
                self.DIRECTION = None
                return
            
        if self.DIRECTION == "down":
            if self.FLOOR > 0:
                self.FLOOR -= 1
                for i in range(110):
                    clock.tick(200)
                    self.y += 1
                    self.rect = pygame.Rect(self.x, self.y, 80, 100)
            else:
                self.DIRECTION = None
                return

    def On(self):
        while self.LIST_UP or self.LIST_DOWN:
            clock.tick(100)
            if self.DIRECTION == "up" and self.FLOOR in self.LIST_UP:
                self.LIST_UP.remove(self.FLOOR)
                clock.tick(1)
            elif self.DIRECTION == "down" and self.FLOOR in self.LIST_DOWN:
                self.LIST_DOWN.remove(self.FLOOR)
                clock.tick(1)
            self.CheckIfRequestToFloor()
            self.TellDirrection()
            self.Move()

        self.MOVING = False

    def Draw(self, assets):
        screen.blit(self.elevator_shaft, (BASE_WIDTH//2-50, 10))
        pygame.draw.rect(screen, assets.BLACK[3], self.rect)