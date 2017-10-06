from random import randint
import os
import pygame


rows = 8
columns = 8
mine_count = 10
exploded = False
mines = []
revealed = []
flagged = []
_image_library = {}
grid = [[]] * rows

for row in range(rows):
    grid[row] = [-1] * columns


def count_bombs_around(row, col):
    bombs = 0

    if (row - 1, col - 1) in mines:
        bombs = bombs + 1
    if (row - 1, col) in mines:
        bombs = bombs + 1
    if (row - 1, col + 1) in mines:
        bombs = bombs + 1

    if (row, col - 1) in mines:
        bombs = bombs + 1
    if (row, col + 1) in mines:
        bombs = bombs + 1

    if (row + 1, col - 1) in mines:
        bombs = bombs + 1
    if (row + 1, col) in mines:
        bombs = bombs + 1
    if (row + 1, col + 1) in mines:
        bombs = bombs + 1

    return bombs


def click_tile(row, col):
    global exploded

    if (row, col) in flagged:
        return

    if exploded:
        return

    if (row, col) in mines:
        grid[row][col] = -3
        exploded = True
        return

    revealed.append((row, col))

    bombs = count_bombs_around(row, col)

    grid[row][col] = bombs


def toggle_flag(row, col):
    if exploded:
        return

    if (row, col) not in revealed:
        if (row, col) not in flagged:
            flagged.append((row, col))
            grid[row][col] = -2
        else:
            flagged.remove((row, col))
            grid[row][col] = -1


def new_game():
    global mines, exploded, grid

    mines.clear()
    revealed.clear()

    for row in range(rows):
        grid[row] = [-1] * columns

    mine_potential = []
    for row in range(rows):
        for col in range(columns):
            mine_potential.append((row, col))

    for i in range(mine_count):
        chosen = mine_potential[randint(0, len(mine_potential) - 1)]
        mines.append(chosen)
        mine_potential.remove(chosen)

    exploded = False


def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image is None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image


def mouse_in(mouse, min, max):
    if min[0] <= mouse[0] <= max[0]:
        if min[1] <= mouse[1] <= max[1]:
            return True

    return False


def launch_game():
    global grid, exploded

    new_game()

    pygame.init()
    screen = pygame.display.set_mode((180, 208))
    done = False
    clock = pygame.time.Clock()
    dir = os.path.dirname(__file__)

    font = pygame.font.SysFont("Arial", 12)
    f2_to_reset = font.render("F2 = Reset", True, (0, 0, 0))
    version_number = font.render("v1.1.0", True, (0, 0, 0))

    offset_x = 5
    offset_y = 33

    space = 6
    icon = 16

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_F2:
                    new_game()

            if event.type == pygame.MOUSEBUTTONUP:
                if mouse_in(event.pos, (82, 8), (99, 25)):
                    new_game()

                for row in range(rows):
                    r = offset_y + (row * (space + icon))
                    r2 = offset_y + (row * (space + icon)) + icon
                    for col in range(columns):
                        c = offset_x + (col * (space + icon))
                        c2 = offset_x + (col * (space + icon)) + icon
                        if mouse_in(event.pos, (c, r), (c2, r2)):
                            if event.button == 1:
                                click_tile(row, col)
                            elif event.button == 3:
                                toggle_flag(row, col)

        if exploded:
            screen.fill((250, 0, 0))
            screen.blit(get_image(dir + "/images/face_dead.png"), (82, 8))
        else:
            screen.fill((250, 250, 250))
            screen.blit(get_image(dir + "/images/face_normal.png"), (82, 8))

        screen.blit(f2_to_reset, (10, 10))
        screen.blit(version_number, (125, 10))

        for row in range(rows):
            for col in range(columns):
                tile = grid[row][col]

                if tile == -3:
                    image = get_image(dir + "/images/tile_mine.png")
                elif tile == -2:
                    image = get_image(dir + "/images/tile_flag.png")
                elif tile == -1:
                    image = get_image(dir + "/images/tile_plain.png")
                elif tile == 0:
                    image = get_image(dir + "/images/tile_clicked.png")
                elif tile == 1:
                    image = get_image(dir + "/images/tile_1.png")
                elif tile == 2:
                    image = get_image(dir + "/images/tile_2.png")
                elif tile == 3:
                    image = get_image(dir + "/images/tile_3.png")
                elif tile == 4:
                    image = get_image(dir + "/images/tile_4.png")
                elif tile == 5:
                    image = get_image(dir + "/images/tile_5.png")
                elif tile == 6:
                    image = get_image(dir + "/images/tile_6.png")
                elif tile == 7:
                    image = get_image(dir + "/images/tile_7.png")
                else:
                    image = get_image(dir + "/images/tile_8.png")

                screen.blit(
                    image,
                    (
                        offset_x + (col * (space + icon)),
                        offset_y + (row * (space + icon))
                    )
                )

        pygame.display.flip()
        clock.tick(60)


def execute():
    launch_game()


if __name__ == '__main__':
    launch_game()
