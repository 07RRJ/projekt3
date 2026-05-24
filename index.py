import pygame
import sys
from ui.load_assets import Assets
from ui.elements import Button, Text
from logic.elevator import Elevator

pygame.init()

BASE_WIDTH, BASE_HEIGHT = 2000, 1130
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
clock = pygame.time.Clock()

elevator = Elevator()

def Start(assets):
    selectedIdx = None
    runing = True

    buttonRect = (
        pygame.Rect(32+(i%3)*58 if i < 9 else 32+58, BASE_HEIGHT-264+58*(i//3), 50, 50) for i in range(10)
    )

    buttons = []
    for idx, rect in enumerate(buttonRect):
        buttons.append(
            Button(
                Text=f"{idx+1}",
                Rect=rect,
                Font=assets.text_font,
                Colour=assets.BLACK[0]
            )
        )

    directionPos = (
        (
            BASE_WIDTH//2-110 if i % 4 > 1 else BASE_WIDTH//2+60,
            15+i//2*110+60 if i%2 else 35+i//2*110
        ) for i in range(1, 19)
    )

    for idx, pos in enumerate(directionPos):
        if idx%2:
            buttons.append(
                Button(
                    BaseImg=assets.up_button,
                    SelectedImg=assets.up_button_selected,
                    Pos=pos
                )
            )
        else:
            buttons.append(
                Button(
                    BaseImg=assets.down_button,
                    SelectedImg=assets.down_button_selected,
                    Pos=pos
                )
            )

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
                if selectedIdx is not None and selectedIdx != elevator.FLOOR:
                    elevator.AddFloor(selectedIdx)

if __name__ == "__main__":
    screen.fill((1, 1, 1))
    assets = Assets()
    title = assets.text_font.render("loading", True, (255, 255, 255))
    screen.blit(title, (BASE_WIDTH//2-title.get_width()//2, BASE_HEIGHT//2-title.get_height()//2))
    pygame.display.flip()
    elevator.elevator_shaft = assets.shaft
    Start(assets)