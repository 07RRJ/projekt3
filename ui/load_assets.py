import sys, os

class Assets:
    def __init__(self):
        self.text_font_path = self.ResourcePath("corbelb.ttf")
    
    def GetFolder():
        if hasattr(sys, "_MEIPASS"):
            return sys._MEIPASS
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def ResourcePath(self, relative_path):
        return os.path.join(self.GetFolder(), relative_path)