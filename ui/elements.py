import pygame, os, sys
from dataclasses import dataclass
from ui.load_assets import Assets

pygame.init()

BASE_WIDTH, BASE_HEIGHT = 1920, 1080
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
assets = Assets()

@dataclass(slots=True)
class Button:
    text: str
    rect: pygame.Rect
    font: pygame.font.Font
    colour: tuple
    label: bool = False
    label_rect: bool = False

    def __post_init__(self):
        self.label = self.font.render(self.text, True, (255, 255, 255))
        self.label_rect = self.label.get_rect(center=self.rect.center)

    def draw(self, is_selected=False):
        if is_selected:
            highlight_rect = self.rect.inflate(12, 12)
            pygame.draw.rect(screen, (255, 200, 0), highlight_rect, border_radius=8)

        pygame.draw.rect(screen, self.colour, self.rect, border_radius=8)

        screen.blit(self.label, self.label_rect)

def Text(text):
    return assets.text_font.render(text, True, (25, 25, 25))