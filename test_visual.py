from mazegenerator import MazeGenerator
from src_back.maze_loader import loader
from src_back import parsing
from src_back.game import constants
from src_back.game.gamestate import Game_state
from src_back.game.constants import Game_status,Directions
import pygame
import argparse



CELL_SIZE = 30
FPS = 50

BLACK = (10, 10, 18)
BLUE = (35, 75, 220)
WHITE = (245, 245, 245)
YELLOW = (255, 220, 0)
PINK = (255, 120, 190)
CYAN = (0, 220, 230)
ORANGE = (255, 160, 30)
RED = (255, 0, 0)
BLUET = (0, 0, 220)



def parser_args() :
    parser = argparse.ArgumentParser()
    parser.add_argument("input", default="config.json")

    args = parser.parse_args()

    return args

def create_game():
    config_data = parser_args()
    data = parsing.pars_config(config_data.input)

    level = data.levels[0]
    width = level.width
    height = level.height
    seed = data.seed

    maze = loader.load_maze(width, height, seed)

    player_position = loader.get_center_position(width, height)
    corner_position = loader.get_corner_positions(width, height)

    super_pacgums = loader.place_super_pacgums(width, height)
    ghosts_place = loader.place_ghosts(width, height)

    pacgums = loader.place_pacgums(
        maze, data.pacgum, corner_position, data.seed
    )

    count_levels = len(data.levels)

    game_state = Game_state(
        maze,
        width,
        height,
        pacgums,
        super_pacgums,
        player_position,
        ghosts_place,
        0,
        count_levels,
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
    top = y * CELL_SIZE
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
        # Supports (x, y) coordinate pairs.
        x, y = position[0], position[1]

        center = (
            int(x * CELL_SIZE + CELL_SIZE / 2),
            int(y * CELL_SIZE + CELL_SIZE / 2)
        )

        pygame.draw.circle(screen, color, center, radius)



def draw_player(screen, player_data):
    x = int(player_data["x"])
    y = int(player_data["y"])

    center = (
        int(x * CELL_SIZE + CELL_SIZE / 2),
        int(y * CELL_SIZE + CELL_SIZE / 2)
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

    colors = [PINK, CYAN, ORANGE, RED]

    
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
            int(float(x) * CELL_SIZE + CELL_SIZE / 2),
            int(float(y) * CELL_SIZE + CELL_SIZE / 2)
        )
        if ghost["state"] == "frightened":
            colors = [BLUET]

        if ghost["state"] != "eaten":
            pygame.draw.circle(
                screen,
                colors[index % len(colors)],
                center,
                CELL_SIZE // 2 - 3
            )


def main():
    pygame.init()

    game_state, width, height = create_game()

    screen = pygame.display.set_mode(
        (width * CELL_SIZE, height * CELL_SIZE)
    )
    font = pygame.font.SysFont("Arial", 40)

    text_surface = font.render("GAME OVER !", True,(255,255,255))
    text_rect = text_surface.get_rect(center = (width // 2, height // 2))

    pygame.display.set_caption("Pac-Man Backend Tester")

    clock = pygame.time.Clock()
    running = True

    key_directions = {
        pygame.K_UP: "up",
        pygame.K_DOWN: "down",
        pygame.K_LEFT: "left",
        pygame.K_RIGHT: "right",
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
      
        # Your backend controls movement and collision.
        game_state.move_player(dt)

        game_state.update_ghosts_time(0.1)

       
        game_state.check_pacgum_at_player()
        # print("Player:", game_state.player.x, game_state.player.y)
        #print("Pacgums before:", len(game_state.pacgums))
        all_data = game_state.all_data_to_dict()

        game_state.move_ghosts(dt)
        # print("score:",game_state.score)
        # print("super:", game_state.super_pacgums)
        game_state.check_ghost_collision()
        # print("ghosts:", all_data["ghosts"])
        # print("player:",game_state.player.x,game_state.player.y)
        # print("Pacgums after:", len(game_state.pacgums))

        screen.fill(BLACK)

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
            screen.fill((0,0,0))
            screen.blit(text_surface,text_rect)
            

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
