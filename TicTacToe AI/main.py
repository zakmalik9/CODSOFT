# Import Modules
import numpy as np
import pygame
import math
import random
# Initialize PyGame
pygame.init()
# Game Variables
row_count = 3
column_count = 3
cell_size = 100
line_width = 3
cell_offset = 10
cell_radius = cell_size//2 - cell_offset
back_color = (50, 50, 50)
grid_color = (255, 255, 255)
cross_color = (255, 0, 0)
circle_color = (0, 0, 255)
default_piece = 0
player_piece = 1
computer_piece = 2
window_length = 3
# Set Up the Screen
width = column_count * cell_size
height = (row_count + 1) * cell_size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic Tac Toe")

# Create a Matrix of the Specified Size containing all 0s
def create_board():
    brd = np.zeros((row_count, column_count))
    return brd

# Go through the Matrix and draw the grid, if any player pieces then Draw them in
def draw_board(brd):
    pygame.draw.rect(screen, back_color, (0, 0, width, height))
    for col in range(1, column_count):
        pygame.draw.line(screen, grid_color, (col * cell_size, cell_size),
                         (col * cell_size, (row_count+1) * cell_size), line_width)
    for r in range(row_count - 1):
        pygame.draw.line(screen, grid_color, (0, (r+2) * cell_size),
                         (column_count * cell_size, (r+2) * cell_size), line_width)
    for col in range(column_count):
        for r in range(row_count):
            if brd[r][col] == player_piece:
                pygame.draw.line(screen, cross_color, (col * cell_size + cell_offset, (r+1) * cell_size + cell_offset),
                                 ((col+1) * cell_size - cell_offset, (r+2) * cell_size - cell_offset), line_width*3)
                pygame.draw.line(screen, cross_color, (col * cell_size + cell_offset, (r+2) * cell_size - cell_offset),
                                 ((col+1) * cell_size - cell_offset, (r+1) * cell_size + cell_offset), line_width*3)
            if brd[r][col] == computer_piece:
                pygame.draw.circle(screen, circle_color, (col * cell_size + cell_size//2,
                                                          (r+1) * cell_size + cell_size//2), cell_radius, line_width*3)

# Check if a Player won
def winning_move(brd, piece):
    # Check Horizontal
    for r in range(row_count):
        if brd[r][0] == piece and brd[r][1] == piece and brd[r][2] == piece:
            return True
    # Check Vertical
    for col in range(column_count):
        if brd[0][col] == piece and brd[1][col] == piece and brd[2][col] == piece:
            return True
    # Check +Slope Diagonal
    if brd[2][0] == piece and brd[1][1] == piece and brd[0][2] == piece:
        return True
    # Check -Slope Diagonal
    if brd[0][0] == piece and brd[1][1] == piece and brd[2][0] == piece:
        return True

def win_manager(brd):
    label = font.render("", 1, back_color)
    global game_running
    if winning_move(brd, player_piece):
        pygame.draw.rect(screen, grid_color, (0, 0, width, cell_size))
        label = font.render(" Player Wins!!! ", 1, cross_color)
        game_running = False
    elif winning_move(brd, computer_piece):
        pygame.draw.rect(screen, grid_color, (0, 0, width, cell_size))
        label = font.render("Computer Wins...", 1, circle_color)
        game_running = False
    elif len(get_valid_locations(brd)) == 0:
        pygame.draw.rect(screen, grid_color, (0, 0, width, cell_size))
        label = font.render("   Game Draw   ", 1, (0, 0, 0))
        game_running = False
    screen.blit(label, (40, 40))

def get_valid_locations(brd):
    valid_locations = []
    for col in range(column_count):
        for r in range(row_count):
            if brd[r][col] == default_piece:
                valid_locations.append((r, col))
    return valid_locations

def is_terminal_node(brd):
    return winning_move(brd, player_piece) or winning_move(brd, computer_piece) or len(get_valid_locations(brd)) == 0

def evaluate_window(wndw, piece, opp_piece):
    score = 0
    wndw = list(wndw)
    if wndw.count(piece) == 3:
        score += 10000
    elif wndw.count(piece) == 2 and wndw.count(default_piece) == 1:
        score += 5
    if wndw.count(opp_piece) == 3:
        score -= 99
    elif wndw.count(opp_piece) == 2 and wndw.count(default_piece) == 1:
        score -= 4
    return score

def score_position(brd, piece, opp_piece):
    score = 0
    # Score Center
    if brd[1][1] == piece:
        score += 10
    elif brd[1][1] == opp_piece:
        score -= 20
    # Score Horizontal
    for r in range(row_count):
        window = brd[r][:window_length]
        score += evaluate_window(window, piece, opp_piece)
    # Score Vertical
    for col in range(column_count):
        window = brd[:window_length][col]
        score += evaluate_window(window, piece, opp_piece)
    # Score -Diagonal
    window = [brd[i][i] for i in range(window_length)]
    score += evaluate_window(window, piece, opp_piece)
    # Score +Diagonal
    window = [brd[2-i][i] for i in range(window_length)]
    score += evaluate_window(window, piece, opp_piece)
    return score

def minimax_ab(node, depth, piece, opp_piece, alpha=-math.inf, beta=math.inf, maximising_player=True):
    if depth == 0 or is_terminal_node(node):
        return None, None, score_position(node, piece, opp_piece)
    valid_locations = get_valid_locations(node)
    best_r, best_col = random.choice(valid_locations)
    if maximising_player:
        value = -np.Inf
        for r, col in valid_locations:
            brd_copy = node.copy()
            brd_copy[r][col] = piece
            new_score = minimax_ab(brd_copy, depth - 1, piece, opp_piece, alpha, beta, False)[2]
            if new_score > value:
                value = new_score
                best_r = r
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_r, best_col, value
    else:
        value = math.inf
        for r, col in valid_locations:
            brd_copy = node.copy()
            brd_copy[r][col] = opp_piece
            new_score = minimax_ab(brd_copy, depth - 1, piece, opp_piece, alpha, beta, True)[2]
            if new_score < value:
                value = new_score
                best_r = r
                best_col = col
            beta = min(beta, value)
            if beta <= alpha:
                break
        return best_r, best_col, value

board = create_board()
print(board)
turn = random.randint(0, 1)
font = pygame.font.SysFont("monospace", 25)
game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the coordinates of the Click and then Modify it to get the Column % Row Clicked
            click_x = event.pos[0]
            click_y = event.pos[1]
            # Ask for Player Input
            if turn == 0 and game_running:
                column = int(math.floor(click_x / cell_size))
                row = int(math.floor(click_y / cell_size)) - 1
                if row != -1 and board[row][column] == default_piece:
                    board[row][column] = player_piece
                    # Increment the Turn
                    turn = (turn + 1) % 2
    # Update the Game Board
    draw_board(board)
    win_manager(board)
    pygame.display.update()
    # AI
    if turn == 1 and game_running:
        pygame.time.wait(500)
        row, column, _ = minimax_ab(board, 4, computer_piece, player_piece)
        if board[row][column] == default_piece:
            board[row][column] = computer_piece
            # Increment the Turn
            turn = (turn + 1) % 2
    # Update the Game Board
    draw_board(board)
    win_manager(board)
    pygame.display.update()

over_running = True
while over_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            over_running = False
    pygame.display.update()
