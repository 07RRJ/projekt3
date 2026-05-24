import pygame
import sys
from ui.load_assets import Assets
from ui.elements import Button, Text
from logic.elevator import Elevator
from threading import Thread

pygame.init()

BASE_WIDTH, BASE_HEIGHT = 2000, 1130
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
clock = pygame.time.Clock()

elevator = Elevator()

floors = {i:i*110+20 for i in range(10)}
# floors = [i for i in range(10)]

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

        elevator.Draw(assets)

        for idx, btn in enumerate(buttons):
            btn.draw(idx == selectedIdx)

        screen.blit(elevator.GOING, (30, 30))

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
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if selectedIdx in floors.keys():
                    if elevator.FLOOR < selectedIdx and selectedIdx not in elevator.LIST_UP:
                        elevator.LIST_UP.append(selectedIdx)
                    elif elevator.FLOOR > selectedIdx and selectedIdx not in elevator.LIST_DOWN:
                        elevator.LIST_DOWN.append(selectedIdx)
                    
                    elevator.TellDirrection()

                    if elevator.MOVING == False:
                        Thread(target=elevator.On).start()
                        elevator.MOVING = True

if __name__ == "__main__":
    screen.fill((1, 1, 1))
    assets = Assets()
    title = assets.text_font.render("loading", True, (255, 255, 255))
    screen.blit(title, (BASE_WIDTH//2-title.get_width()//2, BASE_HEIGHT//2-title.get_height()//2))
    pygame.display.flip()
    elevator.elevator_shaft = assets.shaft
    Start(assets)