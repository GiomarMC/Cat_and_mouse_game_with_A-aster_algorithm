import pygame
from maze_generator import MazeGenerator
import random
from a_star import a_star


class GameMap:
    def __init__(self, width=15, height=15):
        self.maze_generator = MazeGenerator(width, height)
        self.grid, self.cheese_pos = self.maze_generator.generate_maze()
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.cell_size = 40  # Reduced cell size to fit the larger map

    def draw(self, screen):
        for y in range(self.rows):
            for x in range(self.cols):
                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                if self.grid[y][x] == 0:
                    # piso
                    pygame.draw.rect(screen, (222, 184, 135), rect)  # Pino claro
                else:
                    # dibuja solo un borde más fino del muro
                    margin = self.cell_size // 6  # ajusta para grosor
                    wall_rect = pygame.Rect(
                        rect.x + margin,
                        rect.y + margin,
                        self.cell_size - 2 * margin,
                        self.cell_size - 2 * margin
                    )
                    pygame.draw.rect(screen, (100, 60, 60), wall_rect, border_radius=4)


    def is_wall(self, x, y):
        return self.grid[y][x] == 1

    def get_cheese_pos(self):
        return self.cheese_pos

    def get_valid_start_position(self, corner='top_left'):
        """
        Obtiene una posición inicial válida y conectada
        en la esquina especificada.
        """
        valid_positions = []
        if corner == 'top_left':
            for y in range(1, self.rows // 3):
                for x in range(1, self.cols // 3):
                    if not self.is_wall(x, y):
                        valid_positions.append((x, y))
        elif corner == 'bottom_right':
            for y in range(self.rows-2, self.rows - self.rows // 3 - 1, -1):
                for x in range(
                    self.cols-2,
                    self.cols - self.cols // 3 - 1,
                    -1
                ):
                    if not self.is_wall(x, y):
                        valid_positions.append((x, y))
        # Verificar conectividad con el queso
        connected_positions = []
        for pos in valid_positions:
            path = a_star(pos, self.cheese_pos, self.grid)
            if path and len(path) > 1:
                connected_positions.append(pos)
        if not connected_positions:
            # Si no hay posiciones conectadas, regenerar el mapa
            self.grid, self.cheese_pos = self.maze_generator.generate_maze()
            return self.get_valid_start_position(corner)
        return random.choice(connected_positions)
