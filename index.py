import pygame
import sys
from ui.load_assets import Assets
from ui.elements import Button
from threading import Thread

pygame.init()

BASE_WIDTH, BASE_HEIGHT = 2000, 1130
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
clock = pygame.time.Clock()

class Elevator:
    DIRECTION: bool = None
    FLOOR: int = 0
    STOPING_ON_FLOOR: bool = False
    LIST_UP: list = []
    LIST_DOWN: list = []
    x: int = BASE_WIDTH//2-40
    y: int = BASE_HEIGHT-120
    rect_formula: str = "pygame.Rect(self.x, self.y, 80, 100)"
    rect: pygame.rect = pygame.Rect(x, y, 80, 100)
    elevator_shaft = pygame.Rect(BASE_WIDTH//2-50, 10, 100, BASE_HEIGHT-20)

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
                for i in range(110):
                    clock.tick(100)
                    self.y -= 1
                    self.rect = eval(self.rect_formula)
                self.FLOOR += 1
            else:
                self.DIRECTION = None
            
        if self.DIRECTION == "down":
            if self.FLOOR > 0:
                for i in range(110):
                    clock.tick(100)
                    self.y -= 1
                    self.rect = eval(self.rect_formula)
                self.FLOOR -= 1
            else:
                self.DIRECTION = None

    def On(self):
        print()
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

    def Draw(self):
        pygame.draw.rect(screen, assets.BLACK[2], self.elevator_shaft)
        pygame.draw.rect(screen, assets.BLACK[3], self.rect)

elevator = Elevator()

# floors = {i:i*110+20 for i in range(10)}
floors = [i for i in range(10)]

thread = Thread(target=elevator.On)

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
        clock.tick(100)
        screen.fill(assets.BLACK[4])

        elevator.Draw()

        for idx, btn in enumerate(buttons):
            btn.draw(idx == selectedIdx)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            pos = pygame.mouse.get_pos()
            selectedIdx = None
            for idx, btn in enumerate(buttons):
                if btn.rect.collidepoint(pos):
                    selectedIdx = idx
                    print(selectedIdx)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if elevator.FLOOR < selectedIdx and selectedIdx not in elevator.LIST_UP:
                    elevator.LIST_UP.append(selectedIdx)
                elif elevator.FLOOR > selectedIdx and selectedIdx not in elevator.LIST_DOWN:
                    elevator.LIST_DOWN.append(selectedIdx)

if __name__ == "__main__":
    screen.fill((1, 1, 1))
    assets = Assets()
    title = assets.text_font.render("loading", True, (255, 255, 255))
    screen.blit(title, (BASE_WIDTH//2-title.get_width()//2, BASE_HEIGHT//2-title.get_height()//2))
    pygame.display.flip()
    Start(assets)