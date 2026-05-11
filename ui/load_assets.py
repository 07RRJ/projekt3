import sys, os, pygame

pygame.init()

def GetFolder():
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ResourcePath(relative_path):
    return os.path.join(GetFolder(), relative_path)

class Assets:
    BLACK   = ((10, 10, 10), (50, 50, 50), (100, 100, 100), (150, 150, 150), (200, 200, 200), (250, 250, 250))
    RED     = ((100, 30, 30), (150, 50, 50), (200, 50, 50), (250, 75, 75))
    GREEN   = ((30, 100, 30), (30, 150, 30), (30, 200, 30), (50, 250, 50))
    BLUE    = ((30, 30, 100), (30, 30, 150), (30, 30, 200), (30, 30, 250), (173, 216, 230))
    YELLOW  = ((253, 253, 150), (255, 250, 50), (220, 220, 50), (250, 150, 0))

    def __init__(self):
        self.text_font = pygame.font.Font(ResourcePath("ui/assets/fonts/corbelb.ttf"), 24)