from a_star import a_star
import pygame


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.path = []

    def update_path(self, target_pos, game_map):
        self.path = a_star((self.x, self.y), target_pos, game_map.grid)

    def follow_path(self):
        if self.path and len(self.path) > 1:
            self.x, self.y = self.path[1]  # Avanza al siguiente nodo

    def draw(self, screen, cell_size):
        pygame.draw.circle(
            screen,
            (255, 0, 0),
            (self.x * cell_size + cell_size//2,
             self.y * cell_size + cell_size//2),
            cell_size//3
        )
