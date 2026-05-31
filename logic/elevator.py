import pygame
from ui.elements import Text
from threading import Thread, Lock

BASE_WIDTH, BASE_HEIGHT = 2000, 1130
screen = pygame.display.set_mode((BASE_WIDTH, BASE_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
clock = pygame.time.Clock()

floors = {i:i*110+20 for i in range(10)}
dirrectionKeys = {i: ("up" if i%2 else "down", 9-(i-9)//2) for i in range(10, 28)}

DOOR_TIME = 80

class Elevator:
    _lock = Lock()
    DIRECTION: str = None
    MOVING: bool = False
    GOING = Text("On floor: 1")
    FLOOR: int = 0

    LIST_CABIN: list = []
    LIST_UP: list = []
    LIST_DOWN: list = []

    elevator_shaft = None

    def __init__(self):
        self.x: int = BASE_WIDTH // 2 - 40
        self.y: int = BASE_HEIGHT - 120
        self.rect: pygame.Rect = pygame.Rect(self.x, self.y, 80, 100)

    def add_floor(self, floor):
        if floor in floors:
            if floor != self.FLOOR and floor not in self.LIST_CABIN:
                self.LIST_CABIN.append(floor)

        elif floor in dirrectionKeys:
            direction, target = dirrectionKeys[floor]
            if direction == "up" and target not in self.LIST_UP:
                self.LIST_UP.append(target)
            elif direction == "down" and target not in self.LIST_DOWN:
                self.LIST_DOWN.append(target)
        else:
            return

        self.update_dirrection()
        self.tell_dirrection()

        with self._lock:
            if not self.MOVING:
                Thread(target=self.On, daemon=True).start()
                self.MOVING = True

    def update_dirrection(self):
        all_floors = set(self.LIST_CABIN + self.LIST_UP + self.LIST_DOWN)

        if not all_floors:
            self.DIRECTION = None
            return

        above = [floor for floor in all_floors if floor > self.FLOOR]
        below = [floor for floor in all_floors if floor < self.FLOOR]
        here = self.FLOOR in all_floors

        if self.DIRECTION == "up":
            if above:
                return
            if below or here:
                self.DIRECTION = "down"
            else:
                self.DIRECTION = None

        elif self.DIRECTION == "down":
            if below:
                return
            if above or here:
                self.DIRECTION = "up"
            else:
                self.DIRECTION = None

        else:
            if above:
                self.DIRECTION = "up"
            elif below:
                self.DIRECTION = "down"

    def should_stop_here(self):
        floor = self.FLOOR

        if floor in self.LIST_CABIN:
            return True

        if self.DIRECTION == "up" and floor in self.LIST_UP:
            return True
        if self.DIRECTION == "down" and floor in self.LIST_DOWN:
            return True

        if floor == 9 and floor in self.LIST_DOWN:
            self.DIRECTION = "down"
            return True
        if floor == 0 and floor in self.LIST_UP:
            self.DIRECTION = "up"
            return True

        return False

    def clear_current_floor(self):
        floor = self.FLOOR

        if floor in self.LIST_CABIN:
            self.LIST_CABIN.remove(floor)

        if self.DIRECTION == "up" and floor in self.LIST_UP:
            self.LIST_UP.remove(floor)
        elif self.DIRECTION == "down" and floor in self.LIST_DOWN:
            self.LIST_DOWN.remove(floor)

    def tell_dirrection(self):
        all_floors = set(self.LIST_CABIN + self.LIST_UP + self.LIST_DOWN)
        if self.DIRECTION == "up":
            ahead = [floor for floor in all_floors if floor > self.FLOOR]
            target = (min(ahead) + 1) if ahead else (self.FLOOR + 1)
            text = f"Moving up to floor: {target}"
        elif self.DIRECTION == "down":
            ahead = [floor for floor in all_floors if floor < self.FLOOR]
            target = (max(ahead) + 1) if ahead else (self.FLOOR + 1)
            text = f"Moving down to floor: {target}"
        else:
            text = f"On floor: {self.FLOOR + 1}"
        self.GOING = Text(text)

    def move(self):
        if self.DIRECTION == "up":
            if self.FLOOR < 9:
                self.FLOOR += 1
                for _ in range(110):
                    clock.tick(200)
                    self.y -= 1
                    self.rect = pygame.Rect(self.x, self.y, 80, 100)
            else:
                self.update_dirrection()

        elif self.DIRECTION == "down":
            if self.FLOOR > 0:
                self.FLOOR -= 1
                for _ in range(110):
                    clock.tick(200)
                    self.y += 1
                    self.rect = pygame.Rect(self.x, self.y, 80, 100)
            else:
                self.update_dirrection()

    def On(self):
        while self.LIST_CABIN or self.LIST_UP or self.LIST_DOWN:
            clock.tick(100)

            if self.should_stop_here():
                self.clear_current_floor()
                for _ in range(DOOR_TIME):
                    clock.tick(100)

            self.update_dirrection()
            self.tell_dirrection()

            if not (self.LIST_CABIN or self.LIST_UP or self.LIST_DOWN):
                break

            if self.DIRECTION is not None:
                self.move()

        self.MOVING = False
        self.DIRECTION = None
        self.tell_dirrection()

    def draw(self, assets):
        screen.blit(self.elevator_shaft, (BASE_WIDTH // 2 - 50, 10))
        pygame.draw.rect(screen, assets.BLACK[3], self.rect)