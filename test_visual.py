
from mazegenerator import MazeGenerator
from src_back.maze_loader import loader
from src_back import parsing
from src_back.game import constants
from src_back.game.gamestate import Game_state
from src_back.game.constants import Game_status, Directions
import pygame
import argparse
import sys


CELL_SIZE = 30
FPS = 50
TOP_BAR = 50

BLACK = (10, 10, 18)
BLUE = (35, 75, 220)
WHITE = (245, 245, 245)
YELLOW = (255, 220, 0)
PINK = (255, 120, 190)
CYAN = (0, 220, 230)
ORANGE = (255, 160, 30)
RED = (255, 0, 0)
BLUET = (0, 0, 220)


def parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        default="config.json"
    )
    args = parser.parse_args()
    return args


def create_game():
    config_data = parser_args()
    data = parsing.pars_config(config_data.input)

    level = data.levels[0]
    width = level.width
    height = level.height
    seed = data.seed

    grid = loader.load_maze(width, height, seed)

    # maze = grid.maze
    player_position = loader.get_center_position(width, height)
    corner_position = loader.get_corner_positions(width, height)

    super_pacgums = loader.place_super_pacgums(width, height)
    ghosts_place = loader.place_ghosts(width, height)

    pacgums = loader.place_pacgums(
        grid.maze, data.pacgum, corner_position, data.seed
    )

    count_levels = len(data.levels)

    game_state = Game_state(
        grid,
        width,
        height,
        pacgums,
        super_pacgums,
        player_position,
        ghosts_place,
        0,
        1,
        data.level_max_time,
        Game_status.PLAYING,
        False,
        {},
        data,
        []
    )

    game_state.initialize_level()

    return game_state, width, height


def draw_cell_walls(screen, maze, x, y):
    left = x * CELL_SIZE
    top = y * CELL_SIZE + TOP_BAR
    right = left + CELL_SIZE
    bottom = top + CELL_SIZE

    wall_checks = [
        (Directions.UP, (left, top), (right, top)),
        (Directions.RIGHT, (right, top), (right, bottom)),
        (Directions.DOWN, (left, bottom), (right, bottom)),
        (Directions.LEFT, (left, top), (left, bottom)),
    ]

    for direction, start, end in wall_checks:
        if loader.has_wall(maze, x, y, direction):
            pygame.draw.line(screen, BLUE, start, end, 2)


def draw_pellets(screen, positions, color, radius):
    if not positions:
        return

    for position in positions:
        x, y = position[0], position[1]

        center = (
            int(x * CELL_SIZE + CELL_SIZE / 2),
            int(y * CELL_SIZE + TOP_BAR + CELL_SIZE / 2)
        )

        pygame.draw.circle(screen, color, center, radius)


def draw_player(screen, player_data):
    x = player_data["x"]
    y = player_data["y"]

    center = (
        int(x * CELL_SIZE + CELL_SIZE / 2),
        int(y * CELL_SIZE + TOP_BAR + CELL_SIZE / 2)
    )

    pygame.draw.circle(
        screen,
        YELLOW,
        center,
        CELL_SIZE // 2 - 6
    )


def draw_ghosts(screen, ghosts_data):
    if not ghosts_data:
        return

    colors = [CYAN, PINK, ORANGE, RED]

    if isinstance(ghosts_data, dict):
        ghosts = ghosts_data.values()
    else:
        ghosts = ghosts_data

    for index, ghost in enumerate(ghosts):
        if isinstance(ghost, dict):
            x = ghost.get("x")
            y = ghost.get("y")
        else:
            x, y = ghost[0], ghost[1]

        if x is None or y is None:
            continue

        center = (
            int(x * CELL_SIZE + CELL_SIZE / 2),
            int(y * CELL_SIZE + TOP_BAR + CELL_SIZE / 2)
        )

        if isinstance(ghost, dict):
            state = ghost.get("state")
        else:
            state = None

        ghost_color = colors[index % len(colors)]

        if state == "frightened":
            ghost_color = BLUET

        if state != "eaten":
            pygame.draw.circle(
                screen,
                ghost_color,
                center,
                CELL_SIZE // 2 - 3
            )


def main():
    pygame.init()

    game_state, width, height = create_game()

    screen = pygame.display.set_mode(
        (width * CELL_SIZE, height * CELL_SIZE + TOP_BAR)
    )

    ui_font = pygame.font.SysFont("Arial", 24)
    game_over_font = pygame.font.SysFont("Arial", 40)

    text_surface = game_over_font.render(
        "GAME OVER !", True, WHITE
    )
    text_rect = text_surface.get_rect(
        center=(width * CELL_SIZE // 2,
                (height * CELL_SIZE + TOP_BAR) // 2)
    )


    uo_font = pygame.font.SysFont("Arial", 24)
    game_victory_font = pygame.font.SysFont("Arial", 40)

    text_victory = game_victory_font.render(
        "You Win", True, WHITE
    )
    text_rect = text_victory.get_rect(
        center=(width * CELL_SIZE // 2,
                (height * CELL_SIZE + TOP_BAR) // 2)
    )


    pygame.display.set_caption("Pac-Man Backend Tester")

    clock = pygame.time.Clock()
    running = True

    key_directions = {
        pygame.K_UP: "up",
        pygame.K_DOWN: "down",
        pygame.K_LEFT: "left",
        pygame.K_RIGHT: "right",
        
    }

    cheat_key = {
        pygame.K_c : "cheat1",
        pygame.K_l : "cheat2",
    }

    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key in key_directions:
                    game_state.handle_input(
                        key_directions[event.key]
                    )
                elif  event.key in cheat_key:
                    if event.key ==  pygame.K_c:
                        game_state.cheat_skip_level()
                    elif event.key ==  pygame.K_l:
                        game_state.cheat_add_lives()

        all_data = game_state.all_data_to_dict()
        game_state.move_player(dt)
        game_state.check_pacgum_at_player()
        game_state.update_ghosts_time(0.1)
        # game_state.move_ghosts(dt)
        # game_state.ghosts_ai()
        game_state.check_ghost_collision()
        game_state.check_level_complete()

        screen.fill(BLACK)

        # Score and level bar
        score = game_state.score
        

        score_surface = ui_font.render(
            f"Score: {score}", True, WHITE
        )
        level_surface = ui_font.render(
            f"Level: {game_state.level}", True, WHITE
        )
        lives_surface = ui_font.render(
            f"lives: {game_state.player.lives}", True, WHITE
        )
        screen.blit(score_surface, (10, 10))

        screen.blit(lives_surface, (150, 10))
        level_rect = level_surface.get_rect(
            topright=(width * CELL_SIZE - 10, 10)
        )
        screen.blit(level_surface, level_rect)

        # Draw maze
        maze = all_data["maze"]

        for y in range(height):
            for x in range(width):
                draw_cell_walls(screen, maze, x, y)

        draw_pellets(
            screen,
            all_data.get("pacgums", []),
            WHITE,
            3
        )

        draw_pellets(
            screen,
            all_data.get("super_pacgums", []),
            WHITE,
            7
        )

        draw_ghosts(
            screen,
            all_data.get("ghosts", [])
        )

        draw_player(screen, all_data["player"])

        if game_state.game_status == Game_status.GAME_OVER:
            screen.fill(BLACK)
            screen.blit(text_surface, text_rect)
        if game_state.game_status == Game_status.VICTORY:
            screen.fill(BLUE)
            screen.blit(text_victory, text_rect)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
