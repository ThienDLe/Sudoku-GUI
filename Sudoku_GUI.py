import pygame
pygame.init()
pygame.font.init()
pygame.init()


# ---------
# CONSTANTS
# ---------
BOARD = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

TADA = pygame.mixer.Sound(
    '/Users/lethien/Desktop/Projects/Sudoku/tada.mp3')
WIDTH, HEIGHT = 570, 570

GRID_WIDTH = GRID_HEIGHT = 570

BLUE = (2, 69, 107)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (228, 233, 242)
ORANGE = (230, 128, 106)


ROW = COL = 9
GAP = WIDTH // 9

GRID_THICKNESS = 1
BOX_LINE = 5
BORDER_THICKNESS = 9

NUM_FONT = pygame.font.SysFont('couriernew', 40)

TIME_X, TIME_Y = 300, 600

# Get the position of shown numbers from the board
LOCK_POSITION = []
for r in range(ROW):
    for c in range(COL):
        if BOARD[r][c] != 0:
            LOCK_POSITION.append([r, c])

# ------
# WINDOW
# ------
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SUDOKU')


# ---------------
#  GAME FUNCTIONS
# ---------------
def get_location(clicked_x, clicked_y):
    global pos_x
    pos_x = clicked_x // GAP
    global pos_y
    pos_y = clicked_y // GAP


def draw_window(board):
    WIN.fill(WHITE)
    color_locked_num()
    draw_grid_and_borders()
    show_num(board)


def draw_grid_and_borders():
    # Draw lines horizontally and verticallyto form grid
    for i in range(10):
        if i % 3 == 0:
            line_thickness = 5
        else:
            line_thickness = 1
        # Horizontal lines
        pygame.draw.line(WIN, BLACK, (0, GAP * i),
                         (WIDTH, GAP * i), line_thickness)
        # Vertical lines
        pygame.draw.line(WIN, BLACK, (GAP * i, 0),
                         (GAP * i, GAP * 9), line_thickness)


def color_locked_num():
    for row in range(ROW):
        for col in range(COL):
            if [col, row] in LOCK_POSITION:
                locked_num_highlight = pygame.Rect(
                    row * GAP, col * GAP, GAP, GAP)
                pygame.draw.rect(WIN, LIGHT_BLUE, locked_num_highlight)


def show_num(board):
    for row in range(ROW):
        for col in range(COL):
            num = board[col][row]
            if num != 0:
                num_on_board = NUM_FONT.render(str(num), 1, BLUE)
                WIN.blit(num_on_board, (row * GAP + 20, col * GAP + 10))


def draw_box():
    for i in range(2):
        # Vertical lines
        pygame.draw.line(WIN, ORANGE, (pos_x * GAP + i * GAP, pos_y * GAP),
                         (pos_x * GAP + i * GAP, pos_y * GAP + GAP), BOX_LINE)
        # Horizontal lines
        pygame.draw.line(WIN, ORANGE, (pos_x * GAP, pos_y * GAP + i * GAP),
                         (pos_x * GAP + GAP, pos_y * GAP + i * GAP), BOX_LINE)


def update_num(board, val):
    row = pos_x * GAP // GAP
    col = pos_y * GAP // GAP
    if [col, row] in LOCK_POSITION:
        board[col][row] = BOARD[col][row]
    elif val != 0:
        board[col][row] = val

    show_num(board)


def clear_num(board, x, y):
    row = pos_x * GAP // GAP
    col = pos_y * GAP // GAP
    if not [col, row] in LOCK_POSITION:
        board[col][row] = 0
    show_num(board)


def hight_light(board, val):
    if val == 0:
        draw_window(board)
        draw_box()
    else:
        for row in range(ROW):
            for col in range(COL):
                num = board[col][row]
                if num == val:
                    for i in range(2):
                        # Vertical lines
                        pygame.draw.line(WIN, ORANGE, (row * GAP + i * GAP, col * GAP),
                                         (row * GAP + i * GAP, col * GAP + GAP), BOX_LINE)
                        # Horizontal lines
                        pygame.draw.line(WIN, ORANGE, (row * GAP, col * GAP + i * GAP),
                                         (row * GAP + GAP, col * GAP + i * GAP), BOX_LINE)


def move_box(board):
    draw_window(board)
    draw_box()


def find_next_empty(puzzle):
    # Find an empty square and return the [row][col] of it. The empty square is rep by -1.
    # If no empty square, return None, None
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == 0:
                return r, c

    return None, None


def isValid(puzzle, guess, row, col):
    # Check if the guess at row/col is valid. If yes, return True, if not, return False

    # Check the row
    row_vals = puzzle[row]
    if guess in row_vals:
        return False

    # Check the column
    col_vals = [puzzle[r][col] for r in range(9)]
    if guess in col_vals:
        return False

    # Check the square
    # this is the row position of the first square in that cell
    row_start = (row // 3) * 3
    col_start = (col // 3) * 3

    for r in range(col_start, col_start + 3):
        for c in range(row_start, row_start + 3):
            if guess == puzzle[row_start][col_start] and (r, c) != (row, col):
                return False

    # If we get here, the guess is valid
    return True


def solve_sudoku(puzzle):
    # Step 1: pick an empty square to fill a number
    row, col = find_next_empty(puzzle)

    # Step 1.1: if no empty square left, we are done
    if row is None:
        return True

    # Step 2: if there is an empty square, make a guess from 1 - 9
    for guess in range(1, 10):  # guess between 1 and 9
        # Step 3: check if the guess is valid
        if isValid(puzzle, guess, row, col):
            # Step 3.1: place that guess on the square
            puzzle[row][col] = guess
            # Now, recurse using this puzzle
            # Step 4: recursively call our functions
            if solve_sudoku(puzzle):
                return True

            # Step 5: If not valid OR if the guess did not solve the puzzle,
            # then we need to backtrack and try a new number
            puzzle[row][col] = 0  # reset that guess

    # Step 6: if all the numbers do not solve the puzzle, then the puzzle is UNSOLVABLE !!
    return False
# -------------
# MAIN FUNCTION
# -------------


def main():
    run = True
    key = 0
    press_num = False
    click_on_board = False
    last_clicked = (None, None)

    draw_window(BOARD)
    while run:
        pygame.display.update()
        for event in pygame.event.get():
            # Quit the game window
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_on_board = True
                pos_x, pos_y = pygame.mouse.get_pos()
                get_location(pos_x, pos_y)

                if last_clicked != (pos_x, pos_y):
                    draw_window(BOARD)
                    draw_box()
                    last_clicked = (pos_x, pos_y)

            if event.type == pygame.KEYDOWN and click_on_board:
                if event.key == pygame.K_1:
                    key = 1
                    press_num = True
                elif event.key == pygame.K_2:
                    key = 2
                    press_num = True
                elif event.key == pygame.K_3:
                    key = 3
                    press_num = True
                elif event.key == pygame.K_4:
                    key = 4
                    press_num = True
                elif event.key == pygame.K_5:
                    key = 5
                    press_num = True
                elif event.key == pygame.K_6:
                    key = 6
                    press_num = True
                elif event.key == pygame.K_7:
                    key = 7
                    press_num = True
                elif event.key == pygame.K_8:
                    key = 8
                    press_num = True
                elif event.key == pygame.K_9:
                    key = 9
                    press_num = True

                if press_num:
                    update_num(BOARD, key)
                    draw_window(BOARD)
                    hight_light(BOARD, key)
                    press_num = False

                if event.key == pygame.K_BACKSPACE:
                    key = 0
                    clear_num(BOARD, pos_x, pos_y)
                    update_num(BOARD, key)
                    draw_window(BOARD)
                    draw_box()

                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()

                if event.key == pygame.K_UP:
                    pos_y -= 1
                    move_box(BOARD)
                elif event.key == pygame.K_DOWN:
                    pos_y += 1
                    move_box(BOARD)
                elif event.key == pygame.K_LEFT:
                    pos_x -= 1
                    move_box(BOARD)
                elif event.key == pygame.K_RIGHT:
                    pos_x += 1
                    move_box(BOARD)

                if event.key == pygame.K_RETURN:
                    solve_sudoku(BOARD)
                    draw_window(BOARD)
                    TADA.play()


# ---------------------
# RUN THE MAIN FUNCTION
# ---------------------
main()
