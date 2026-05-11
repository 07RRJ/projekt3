import pygame, os, sys
from dataclasses import dataclass

pygame.init()

BASE_WIDTH, BASE_HEIGHT = 1920, 1080
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)

@dataclass(slots=True)
class Button:
    def __init__(self, text, rect, assets, ):
        self.text: str = text
        self.rect: pygame.Rect
        self.font: pygame.font.Font = assets.text_font
        self.label: pygame.Surface = None
        self.label_rect: pygame.Rect = None

    def __post_init__(self):
        if self.textColour:
            self.label = self.font.render(self.text, True, (0, 0, 0))
        else:
            self.label = self.font.render(self.text, True, (255, 255, 255))
        self.label_rect = self.label.get_rect(center=self.rect.center)

    def draw(self, is_selected=False):
        if is_selected:
            highlight_rect = self.rect.inflate(12, 12)
            pygame.draw.rect(screen, (255, 200, 0), highlight_rect, border_radius=8)

        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)

        screen.blit(self.label, self.label_rect)