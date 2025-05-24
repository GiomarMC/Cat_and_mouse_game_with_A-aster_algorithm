import random
import numpy as np


class MazeGenerator:
    def __init__(self, width=15, height=15):
        self.width = width
        self.height = height
        self.grid = None
        self.cheese_pos = None

    def generate_maze(self):
        # Inicializar la cuadrícula con muros
        self.grid = np.ones((self.height, self.width), dtype=int)

        # Bordes siempre muros
        self.grid[0, :] = 1
        self.grid[-1, :] = 1
        self.grid[:, 0] = 1
        self.grid[:, -1] = 1

        # Comenzar desde una posición aleatoria interna (no borde)
        start_x = random.randint(1, self.width-2)
        start_y = random.randint(1, self.height-2)

        # Crear caminos usando backtracking recursivo
        self._carve_path(start_x, start_y)

        # Añadir algunos espacios abiertos
        self._add_some_open_spaces()

        # Colocar el queso en una zona accesible
        self._place_cheese()

        return self.grid, self.cheese_pos

    def _carve_path(self, x, y):
        self.grid[y][x] = 0
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (
                1 <= nx < self.width-1 and
                1 <= ny < self.height-1 and
                self.grid[ny][nx] == 1
            ):
                self.grid[y + dy//2][x + dx//2] = 0
                self._carve_path(nx, ny)

    def _add_some_open_spaces(self):
        for _ in range(self.width * self.height // 10):
            x = random.randint(1, self.width-2)
            y = random.randint(1, self.height-2)
            self.grid[y][x] = 0

    def _place_cheese(self):
        accessible_positions = []
        for y in range(1, self.height-1):
            for x in range(1, self.width-1):
                if self.grid[y][x] == 0:
                    accessible_positions.append((x, y))
        if accessible_positions:
            self.cheese_pos = random.choice(accessible_positions)
