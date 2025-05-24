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

player = Player(player_start[0], player_start[1])
enemy = Enemy(enemy_start[0], enemy_start[1])
cheese_pos = game_map.get_cheese_pos()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-1, 0, game_map)
    if keys[pygame.K_RIGHT]:
        player.move(1, 0, game_map)
    if keys[pygame.K_UP]:
        player.move(0, -1, game_map)
    if keys[pygame.K_DOWN]:
        player.move(0, 1, game_map)

    # IA: recalcular ruta y mover al gato
    enemy.update_path((player.x, player.y), game_map)
    enemy.follow_path()

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
    clock.tick(5)

    # Condición de victoria o derrota
    if (player.x, player.y) == (enemy.x, enemy.y):
        print("¡El gato atrapó al ratón!")
        running = False
    if (player.x, player.y) == cheese_pos:
        print("¡El ratón ganó!")
        running = False

pygame.quit()
