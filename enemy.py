from a_star import a_star
import pygame


class Enemy:
    def __init__(self, x, y, cell_size=40, speed=4):
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.speed = speed  # píxeles por frame
        self.pixel_x = x * cell_size
        self.pixel_y = y * cell_size
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.moving = False
        self.path = []

    def update_path(self, target_pos, game_map):
        self.path = a_star((self.x, self.y), target_pos, game_map.grid)

    def follow_path(self):
        if self.moving:
            return
        if self.path and len(self.path) > 1:
            nx, ny = self.path[1]
            self.x, self.y = nx, ny
            self.target_x = nx * self.cell_size
            self.target_y = ny * self.cell_size
            self.moving = True

    def update(self):
        if self.moving:
            dx = self.target_x - self.pixel_x
            dy = self.target_y - self.pixel_y
            step_x = self.speed if dx > 0 else -self.speed
            step_y = self.speed if dy > 0 else -self.speed
            if abs(dx) > 0:
                if abs(dx) < self.speed:
                    self.pixel_x = self.target_x
                else:
                    self.pixel_x += step_x
            if abs(dy) > 0:
                if abs(dy) < self.speed:
                    self.pixel_y = self.target_y
                else:
                    self.pixel_y += step_y
            if self.pixel_x == self.target_x and self.pixel_y == self.target_y:
                self.moving = False

    def draw(self, screen, cell_size):
        pygame.draw.circle(
            screen,
            (255, 0, 0),
            (int(self.pixel_x) + cell_size//2,
             int(self.pixel_y) + cell_size//2),
            cell_size//3
        )
