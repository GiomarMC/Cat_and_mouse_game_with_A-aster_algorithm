import pygame


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy, game_map):
        nx, ny = self.x + dx, self.y + dy
        if (0 <= nx < game_map.cols and
            0 <= ny < game_map.rows and
                not game_map.is_wall(nx, ny)):
            self.x, self.y = nx, ny

    def draw(self, screen, cell_size):
        pygame.draw.circle(
            screen,
            (0, 0, 255),
            (self.x * cell_size + cell_size//2,
             self.y * cell_size + cell_size//2),
            cell_size//3
        )
