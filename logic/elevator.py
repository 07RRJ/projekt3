import pygame
from ui.elements import Text

BASE_WIDTH, BASE_HEIGHT = 2000, 1130 #     elevator_shaft = pygame.Rect(BASE_WIDTH//2-50, 10, 100, BASE_HEIGHT-20)
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
clock = pygame.time.Clock()

floors = {i:i*110+20 for i in range(10)}

class Elevator:
    DIRECTION: bool = None
    MOVING: bool = False
    GOING = Text("On floor: 1")
    FLOOR: int = 0
    STOPING_ON_FLOOR: bool = False
    LIST_UP: list = []
    LIST_DOWN: list = []
    # next_floor: int = FLOOR
    x: int = BASE_WIDTH//2-40
    y: int = BASE_HEIGHT-120
    rect_formula: str = "pygame.Rect(self.x, self.y, 80, 100)"
    rect: pygame.rect = pygame.Rect(x, y, 80, 100)
    elevator_shaft = None
    # elevator_shaft = pygame.Rect(BASE_WIDTH//2-50, 10, 100, BASE_HEIGHT-20)

    def CheckIfRequestToFloor(self):
        if self.DIRECTION == "up" and self.LIST_UP:
            # self.next_floor = min(self.LIST_UP)
            return
        elif self.DIRECTION == "down" and self.LIST_DOWN:
            # self.next_floor = max(self.LIST_DOWN)
            return
        else:
            self.DIRECTION = None
        
        if self.LIST_UP and self.DIRECTION == None:
            self.DIRECTION = "up"
        elif self.LIST_DOWN and self.DIRECTION == None:
            self.DIRECTION = "down"

    def TellDirrection(self):
        text = ""
        if self.DIRECTION == "up":
            text = f"Going up to floor: {min(self.LIST_UP)+1}"
        elif self.DIRECTION == "down":
            text = f"Going down to floor: {max(self.LIST_DOWN)+1}"
        else:
            text = f"On floor: {self.FLOOR+1}"
        self.GOING = Text(text)

    def Move(self):
        if self.DIRECTION == "up":
            if self.FLOOR < 9:
                self.FLOOR += 1
                for i in range(110):
                    clock.tick(100)
                    self.y -= 1
                    self.rect = eval(self.rect_formula)
            else:
                self.DIRECTION = None
            
        if self.DIRECTION == "down":
            if self.FLOOR > 0:
                self.FLOOR -= 1
                for i in range(110):
                    clock.tick(100)
                    self.y += 1
                    self.rect = eval(self.rect_formula)
            else:
                self.DIRECTION = None

    def On(self):
        while self.LIST_UP or self.LIST_DOWN:
            clock.tick(100)
            self.CheckIfRequestToFloor()
            self.TellDirrection()
            self.Move()
            if self.FLOOR in self.LIST_UP:
                clock.tick(1)
                self.LIST_UP.remove(self.FLOOR)
            elif self.FLOOR in self.LIST_DOWN:
                clock.tick(1)
                self.LIST_DOWN.remove(self.FLOOR)
            self.CheckIfRequestToFloor()
            self.TellDirrection()

        self.MOVING = False

    def Draw(self, assets):
        # pygame.draw.rect(screen, assets.BLACK[2], self.elevator_shaft)
        screen.blit(self.elevator_shaft, (BASE_WIDTH//2-50, 10))
        pygame.draw.rect(screen, assets.BLACK[3], self.rect)