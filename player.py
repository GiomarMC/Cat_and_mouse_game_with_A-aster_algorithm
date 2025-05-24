import pygame


class Player:
    def __init__(self, x, y, cell_size=40, speed=6):
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.speed = speed  # píxeles por frame
        self.pixel_x = x * cell_size
        self.pixel_y = y * cell_size
        self.target_x = self.pixel_x
        self.target_y = self.pixel_y
        self.moving = False
        self.move_dir = (0, 0)

    def move(self, dx, dy, game_map):
        if self.moving:
            return  # No aceptar nueva orden hasta terminar movimiento
        nx, ny = self.x + dx, self.y + dy
        if (0 <= nx < game_map.cols and
            0 <= ny < game_map.rows and
                not game_map.is_wall(nx, ny)):
            self.x, self.y = nx, ny
            self.target_x = nx * self.cell_size
            self.target_y = ny * self.cell_size
            self.move_dir = (dx, dy)
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
            (0, 0, 255),
            (int(self.pixel_x) + cell_size//2,
             int(self.pixel_y) + cell_size//2),
            cell_size//3
        )
