import pygame
import random

# utility
renderedMarks = []
renderedMarksCoords_enemy = []
renderedMarksCoords_me = []
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'X', '*']
numbers = ['  1', '  2', '  3', '  4', '  5', '  6', '  7', '  8', '  9', ' 10']
hit_coords = ""
renderedLetters = {}
renderedNumbers = {}


def refresh():
    global direction_hit_coords
    global hit_direction
    global directions
    direction_hit_coords = []
    hit_direction = -1
    directions = [0, 1, 2, 3]


def extra_coords(x, y, type, direction):
    if type == 0:
        # neighbours of item in two-dimensional array
        neighbours = lambda x, y: [(x2, y2) for x2 in range(x - 1, x + 2)
                                   for y2 in range(y - 1, y + 2)
                                   if (-1 < x < 10 and
                                       -1 < y < 10 and
                                       (x != x2 or y != y2) and
                                       (-1 < x2 < 10) and
                                       (-1 < y2 < 10))]
        return neighbours(x, y)
    else:
        coords = []
        if direction == 0:
            for i in range(9-x):
                coords.append([x+i+1, y])
            return coords
        elif direction == 1:
            for i in range(y):
                coords.append([x, y-i-1])
            return coords
        elif direction == 2:
            for i in range(x):
                coords.append([x-i-1, y])
            return coords
        elif direction == 3:
            for i in range(9-y):
                coords.append([x, y+i+1])
            return coords


# game
gameend = False
gamefield = [[0 for i in range(10)] for j in range(10)]
temp_gamefield = [[0 for i in range(10)] for j in range(10)]
possible_coords = []
direction_hit_coords = []
hit_direction = -1
gamefield_enemy = []
gamefield_me = []
ships_enemy = {}
ships_me = {}
shipcount_enemy = 10
shipcount_me = 10
directions = [0, 1, 2, 3]

# game UI
gamefield_x = 36
gamefield_y = 36
w = 30
h = 30
# offset for second field
offset = 400
# end coords of field
gamefield_end_x = gamefield_x + w * (len(letters) - 3)
gamefield_end_y = gamefield_y + h * (len(numbers) - 1)


def make_font(fonts, size):
    available = pygame.font.get_fonts()
    choices = map(lambda x: x.lower().replace(' ', ''), fonts)
    for choice in choices:
        if choice in available:
            return pygame.font.SysFont(choice, size)
    return pygame.font.Font(None, size)


def get_font(font_preference, size):
    global _cached_fonts
    key = str(font_preference) + "|" + str(size)
    font = _cached_fonts.get(key, None)
    if font is None:
        font = make_font(font_preference, size)
        _cached_fonts[key] = font
    return font


def create_text(text, fonts, size, dict):
    if text == "X":
        color = (255, 0, 0)
    else:
        color = (255, 255, 255)
    if text == "You won!" or text == "You lost...":
        key = "endgametext"
    else:
        key = text
    image = dict.get(key, None)
    if image is None:
        font = get_font(fonts, size)
        image = font.render(text, True, color)
        dict[key] = image
    return image


def find_position():
    found = False
    while not found:
        x = random.randint(0, 9)
        row = temp_gamefield[x]
        if list(row).count(0) > 0:
            while True:
                y = random.randint(0, 9)
                if row[y] == 0:
                    break
            found = True
    return [x, y]


def generate_and_save_ship(x, y, direction, shiplength, i, j, side):
    if direction == 0:
        temp_gamefield[x + i][y] = "S"
        coords = (x + i, y)
    elif direction == 1:
        temp_gamefield[x][y - i] = "S"
        coords = (x, y - i)
    elif direction == 2:
        temp_gamefield[x - i][y] = "S"
        coords = (x - i, y)
    elif direction == 3:
        temp_gamefield[x][y + i] = "S"
        coords = (x, y + i)
    key = str(shiplength) + str(j + 1)
    item = ships_enemy.get(key, None) if side == 1 else ships_me.get(key, None)
    if item is None:
        if side == 0:
            ships_me[key] = [coords]
        else:
            ships_enemy[key] = [coords]
    else:
        if side == 0:
            ships_me[key].append(coords)
        else:
            ships_enemy[key].append(coords)


def generate_side(side):
    global directions
    global gamefield_me
    global gamefield_enemy
    global temp_gamefield

    taken_directions = []
    temp_gamefield = [[0 for i in range(10)] for j in range(10)]

    for i in range(4):
        shipcount = i + 1
        shiplength = (5 - shipcount)
        for j in range(shipcount):
            directions = [0, 1, 2, 3]
            placed = False
            c = 0
            while not placed:
                pos = find_position()
                x = pos[0]
                y = pos[1]
                rotated = False
                notfound = False
                while not rotated:
                    if len(directions) > 0:
                        if len(taken_directions) == 4:
                            taken_directions = []
                            break
                        direction = random.choice(directions)
                        taken_directions.append(direction)
                    else:
                        notfound = True
                    if notfound:
                        temp_gamefield[x][y] = "*"
                        placed = True
                        break
                    if direction == 0:
                        error_count = 0
                        if x + shiplength < 10:
                            for i in range(shiplength):
                                if temp_gamefield[x + i][y] != 0:
                                    error_count += 1
                                    break
                            if error_count == 0:
                                placed = True
                                rotated = True
                                for i in range(shiplength):
                                    generate_and_save_ship(x, y, direction, shiplength, i, j, side)
                                add_disabled(x, y, direction, shiplength)
                        else:
                            directions.remove(direction)
                    elif direction == 1:
                        error_count = 0
                        if y - shiplength > -1:
                            for i in range(shiplength):
                                if temp_gamefield[x][y - i] != 0:
                                    error_count += 1
                                    break
                            if error_count == 0:
                                placed = True
                                rotated = True
                                for i in range(shiplength):
                                    generate_and_save_ship(x, y, direction, shiplength, i, j, side)
                                add_disabled(x, y, direction, shiplength)
                        else:
                            directions.remove(direction)
                    elif direction == 2:
                        error_count = 0
                        if x - shiplength > -1:
                            for i in range(shiplength):
                                if temp_gamefield[x - i][y] != 0:
                                    error_count += 1
                                    break
                            if error_count == 0:
                                placed = True
                                rotated = True
                                for i in range(shiplength):
                                    generate_and_save_ship(x, y, direction, shiplength, i, j, side)
                                add_disabled(x, y, direction, shiplength)
                        else:
                            directions.remove(direction)
                    elif direction == 3:
                        error_count = 0
                        if y + shiplength < 10:
                            for i in range(shiplength):
                                if temp_gamefield[x][y + i] != 0:
                                    error_count += 1
                                    break
                            if error_count == 0:
                                placed = True
                                rotated = True
                                for i in range(shiplength):
                                    generate_and_save_ship(x, y, direction, shiplength, i, j, side)
                                add_disabled(x, y, direction, shiplength)
                        else:
                            directions.remove(direction)
    if side == 0:
        gamefield_me = temp_gamefield
    else:
        gamefield_enemy = temp_gamefield


def draw_gamefield():
    for i in range(10):
        key = letters[i]
        letter_width = renderedLetters[key].get_width() // 2
        add = (30 - letter_width) / 2
        screen.blit(renderedLetters[key], ((i + 1) * 30 + add, 0))
        screen.blit(renderedLetters[key], ((i + 1) * 30 + add + offset, 0))
    for i in range(10):
        key = numbers[i]
        number_height = renderedNumbers[key].get_height() // 2
        add = (30 - number_height) / 2
        screen.blit(renderedNumbers[key], (0, 26 + i * 30 + add))
        screen.blit(renderedNumbers[key], (0 + offset, 26 + i * 30 + add))
    shipcolor = (200, 128, 50)
    for i in range(10):
        for j in range(10):
            pygame.draw.rect(screen, color, pygame.Rect(gamefield_x + j * 30, gamefield_y + i * 30, h, w), 1)
            pygame.draw.rect(screen, color, pygame.Rect(gamefield_x + offset + j * 30, gamefield_y + i * 30, h, w), 1)
            if gamefield_me[i][j] == "S":
                pygame.draw.rect(screen, shipcolor, pygame.Rect(gamefield_x + j * 30, gamefield_y + i * 30, h, w), 3)
    for i in range(len(renderedMarks)):
        screen.blit(renderedLetters[renderedMarks[i][0]], renderedMarks[i][1])
    if not gameend:
        create_text(hit_coords, fonts, 18, renderedLetters)
        create_text("Comp last hit: ", fonts, 20, renderedLetters)
        screen.blit(renderedLetters["Comp last hit: "], (30, 400))
        screen.blit(renderedLetters[hit_coords], (170, 402))


def open_cell(x, y, is_destroyed, side):
    global offset
    xcord = x
    ycord = y
    if is_destroyed:
        symbol = "*"
        fix = [3, 2]
    else:
        if not (x < 10 and y < 10):
            xcord = x // 30 - 1
            ycord = y // 30 - 1
        if side == 0:
            if gamefield_enemy[xcord][ycord] == 0 or gamefield_enemy[xcord][ycord] == '*':
                symbol = "*"
            else:
                symbol = "X"
        else:
            if gamefield_me[xcord][ycord] == 0 or gamefield_me[xcord][ycord] == '*':
                symbol = "*"
            else:
                symbol = "X"
        if symbol == "*":
            fix = [3, 2]
        else:
            fix = [2, -4]
    # check if any mark exists in this cell
    if side == 0:
        if sum(1 for elem in renderedMarksCoords_enemy if elem == [xcord, ycord]) != 0:
            return
        renderedMarksCoords_enemy.append([xcord, ycord])
    else:
        if sum(1 for elem in renderedMarksCoords_me if elem == [xcord, ycord]) != 0:
            return
        renderedMarksCoords_me.append([xcord, ycord])

    letter_width = renderedLetters[symbol].get_width() // 2
    letter_height = renderedLetters[symbol].get_height() // 2

    # a little align
    addX = (30 - letter_width) / 2 + fix[0]
    addY = (30 - letter_height) / 2 + fix[1]

    cell_offset = offset if side == 0 else 0
    renderedMarks.append([symbol, (30 + w * ycord + cell_offset + addX, 30 + h * xcord + addY)])
    if symbol == "X":
        if register_hit((xcord, ycord), side) == "D":
            if side == 1: return "D"
        return "X"
    return "*"


def indexbytuple(tupl, value):
    cell = temp_gamefield[tupl[0]][tupl[1]]
    temp_gamefield[tupl[0]][tupl[1]] = value if cell == 0 else cell


def add_disabled(x, y, direction, length):
    for i in range(length):
        if direction == 0:
            nb = extra_coords(x + i, y, 0, None)
        elif direction == 1:
            nb = extra_coords(x, y - i, 0, None)
        elif direction == 2:
            nb = extra_coords(x - i, y, 0, None)
        elif direction == 3:
            nb = extra_coords(x, y + i, 0, None)
        for item in nb:
            indexbytuple(item, "*")


def register_hit(coords, side):
    global ships_me
    global ships_enemy

    status = ""
    temp_ships = ships_me if side == 1 else ships_enemy
    for key, val in temp_ships.items():
        if list(val).count(coords) == 1:
            idx = list(val).index(coords)
            val[idx] = (*val[idx], "D")
            status = check_if_destroyed(key, key[:1], side, temp_ships)
            break
    if side == 1:
        ships_me = temp_ships
    else:
        ships_enemy = temp_ships
    if status == "destroyed":
        return "D"


def check_if_destroyed(key, length, side, dict):
    global shipcount_enemy
    global shipcount_me
    global gameend

    count = sum(1 for item in dict[key] if 'D' in item)
    if count == int(length):
        destroy(key, side, dict)
        if side == 0:
            shipcount_enemy -= 1
        else:
            shipcount_me -= 1
        if shipcount_enemy == 0 or shipcount_me == 0:
            gameend = True
        return "destroyed"


def destroy(key, side, dict):
    for coords in dict[key]:
        neighbours_arr = extra_coords(coords[0], coords[1], 0, None)
        for nb in neighbours_arr:
            if side == 1:
                if possible_coords.count(nb) > 0:
                    possible_coords.remove(nb)
            open_cell(nb[0], nb[1], 1, side)


def do_shot():
    global hit_coords
    global hit_direction
    global directions
    global direction_hit_coords

    hit_coords = ""
    start_x = -1
    start_y = -1
    while True and not gameend:
        if direction_hit_coords:
            coords = direction_hit_coords[0]
        else:
            coords = random.choice(possible_coords)
        x = coords[0]
        y = coords[1]
        if start_x == -1:
            start_x = x
            start_y = y
        if possible_coords.count((x, y)) > 0:
            possible_coords.remove((x, y))
        status = open_cell(x, y, 0, 1)
        if status is not None:
            if hit_coords != "":
                hit_coords += " + "
            hit_coords += letters[y] + str(x + 1)
        #hit_coords = str(len(possible_coords))
        if status != "X" and status != "D":
            if status is not None:
                if direction_hit_coords:
                    directions.remove(hit_direction)
                    if not directions:
                        start_x = -1
                        start_y = -1
                        refresh()
                        continue
                    hit_direction = random.choice(directions)
                    direction_hit_coords = extra_coords(start_x, start_y, 1, hit_direction)
                break
            else:
                if len(direction_hit_coords) > 0:
                    direction_hit_coords.remove(direction_hit_coords[0])
        else:
            if status == "D":
                start_x = -1
                start_y = -1
                refresh()
            else:
                if status == "X":
                    if direction_hit_coords:
                        direction_hit_coords.remove([x, y])
                if not direction_hit_coords:
                    hit_direction = random.choice(directions)
                    direction_hit_coords = extra_coords(start_x, start_y, 1, hit_direction)


pygame.init()

clock = pygame.time.Clock()
_cached_fonts = {}
fonts = ["Comic Sans MS"]

rect_choose = pygame.Rect(gamefield_x + offset, gamefield_y, h, w)

for i in range(len(letters)):
    create_text(letters[i], fonts, 26, renderedLetters)
for i in range(len(numbers)):
    create_text(numbers[i], fonts, 26, renderedNumbers)

screen = pygame.display.set_mode((770, 550))

for i in range(2):
    generate_side(i)

for i in range(10):
    for j in range(10):
        coords = (i, j)
        possible_coords.append(coords)

done = False
test = False
turn = True
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if not gameend:
            if test:
                for i in range(10):
                    for j in range(10):
                        open_cell(rect_choose.y - 6, rect_choose.x - 6 - offset, 0, 0)
                        #open_cell(j, i, 0, 1)
                        rect_choose.move_ip(w, 0)
                    rect_choose = pygame.Rect(gamefield_x + offset, gamefield_y + (i + 1) * 30, h, w)
                test = not test
            if not turn:
                do_shot()
                turn = not turn
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_UP:
                    rect_choose.move_ip(0, -h)
                elif event.key == pygame.K_DOWN:
                    rect_choose.move_ip(0, h)
                elif event.key == pygame.K_LEFT:
                    rect_choose.move_ip(-w, 0)
                elif event.key == pygame.K_RIGHT:
                    rect_choose.move_ip(w, 0)
                elif event.key == pygame.K_RETURN:
                    if open_cell(rect_choose.y - 6, rect_choose.x - 6 - offset, 0, 0) == "*":
                        turn = not turn
                rect_choose.clamp_ip(pygame.Rect(gamefield_x + offset, gamefield_y,
                                                 gamefield_end_x - 6, gamefield_end_y - 6))

        color = (0, 84, 148)
        screen.fill((0, 0, 0))
        draw_gamefield()
        pygame.draw.rect(screen, (255, 255, 0), rect_choose, 2)

        if gameend:
            text = "You won!" if shipcount_enemy == 0 else "You lost..."
            text = create_text(text, fonts, 26, renderedLetters)
            screen.blit(renderedLetters["endgametext"], (400 - text.get_width() // 2, 450 - text.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)
