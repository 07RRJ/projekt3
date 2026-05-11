import pygame
from ui.load_assets import Assets, GetFolder, ResourcePath
from ui.elements import Button

pygame.init()

BASE_WIDTH, BASE_HEIGHT = 1920, 1080
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
clock = pygame.time.Clock()

class Elevator:
    DIRECTION = None
    FLOOR = 0
    STOPING_ON_FLOOR = False
    LIST_UP = []
    LIST_DOWN = []

    def CheckIfRequestToFloor(self):
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
            if self.FLOOR < 9:
                self.FLOOR += 1
            else:
                self.DIRECTION = None
            
        if self.DIRECTION == "down":
            if self.FLOOR > 0:
                self.FLOOR -= 1
            else:
                self.DIRECTION = None

    def On(self):
        print(self.FLOOR, self.DIRECTION, self.LIST_UP, self.LIST_DOWN)
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

def Start(assets):
    selectedIdx = None
    runing = True

    ButtonRect = (
        pygame.Rect(32, BASE_HEIGHT-62*i, 100, 30) for i in range(1, 11)
    )

    buttons = []
    for idx, rect in enumerate(ButtonRect):
        buttons.append(Button(f"{idx+1}", rect, assets.text_font, assets.BLACK[0]))

    while runing:
        for y in range(10):
            clock.tick(1)
            screen.fill(assets.BLACK[4])

            elevator_shaft = pygame.Rect(BASE_WIDTH//2-50, BASE_HEIGHT//12, 100, BASE_HEIGHT//12*10)
            elevator = pygame.Rect(BASE_WIDTH//2-40, BASE_HEIGHT-BASE_HEIGHT//12*10-y*100, 80, 120)

            pygame.draw.rect(screen, assets.BLACK[2], elevator_shaft)
            pygame.draw.rect(screen, assets.BLACK[3], elevator)

            for button in buttons:
                button.draw()

            pygame.display.flip()

if __name__ == "__main__":
    screen.fill((1, 1, 1))
    pygame.display.flip()
    assets = Assets()
    Start(assets)