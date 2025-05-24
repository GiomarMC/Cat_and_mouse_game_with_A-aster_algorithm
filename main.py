import pygame
from game_map import GameMap
from player import Player
from enemy import Enemy

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

game_map = GameMap(15, 15)

# Obtener posiciones iniciales válidas
player_start = game_map.get_valid_start_position('top_left')
enemy_start = game_map.get_valid_start_position('bottom_right')

player = Player(player_start[0], player_start[1], game_map.cell_size, speed=6)
enemy = Enemy(enemy_start[0], enemy_start[1], game_map.cell_size, speed=4)
cheese_pos = game_map.get_cheese_pos()

move_dir = [0, 0]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_dir = [-1, 0]
            elif event.key == pygame.K_RIGHT:
                move_dir = [1, 0]
            elif event.key == pygame.K_UP:
                move_dir = [0, -1]
            elif event.key == pygame.K_DOWN:
                move_dir = [0, 1]
        elif event.type == pygame.KEYUP:
            if event.key in [
                pygame.K_LEFT, pygame.K_RIGHT,
                pygame.K_UP, pygame.K_DOWN
            ]:
                move_dir = [0, 0]

    # Movimiento continuo del jugador
    if move_dir != [0, 0] and not player.moving:
        player.move(move_dir[0], move_dir[1], game_map)

    player.update()

    # IA: recalcular ruta y mover al gato solo si no está moviéndose
    if not enemy.moving:
        enemy.update_path((player.x, player.y), game_map)
        enemy.follow_path()
    enemy.update()

    # Dibujar
    screen.fill((0, 0, 0))
    game_map.draw(screen)
    player.draw(screen, game_map.cell_size)
    enemy.draw(screen, game_map.cell_size)
    pygame.draw.circle(
        screen,
        (255, 255, 0),
        (cheese_pos[0]*game_map.cell_size + game_map.cell_size//2,
         cheese_pos[1]*game_map.cell_size + game_map.cell_size//2),
        game_map.cell_size//3
    )
    pygame.display.flip()
    clock.tick(60)

    # Condición de victoria o derrota
    if (player.x, player.y) == (enemy.x, enemy.y):
        print("¡El gato atrapó al ratón!")
        running = False
    if (player.x, player.y) == cheese_pos:
        print("¡El ratón ganó!")
        running = False

pygame.quit()
