import pygame
import os
import sys
from pygame.locals import *
from random import randrange

pygame.font.init()
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

WIDTH, HEIGHT = 450, 450
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# the board (a 2d list) is being initialized with zeros representing free spots
board = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60


def fill_board():
    for i in range(0, 27):
        row = randrange(0, 9)
        col = randrange(0, 9)
        num = randrange(1, 10)
        while not check_valid(row, col, num):
            row = randrange(0, 9)
            col = randrange(0, 9)
            num = randrange(1, 10)
        board[row][col] = num


def draw_window():
    WIN.fill(WHITE)
    pygame.display.update()
    for i in range(1, 9):
        if i % 3 == 0:
            thickness = 3
        else:
            thickness = 2
        pygame.draw.line(WIN, BLACK, (450 / 9 * i, 0), (450 / 9 * i, 450), thickness)
        pygame.draw.line(WIN, BLACK, (0, 450 / 9 * i), (450, 450 / 9 * i), thickness)

    for i in range(1, 10):
        for j in range(1, 10):
            if board[i - 1][j - 1] != 0:
                font = pygame.font.Font(None, 30)
                text = font.render(str(board[i - 1][j - 1]), True, BLACK, WHITE)
                textRect = text.get_rect()
                textRect.center = ((450 / 9) * j - 25, (450 / 9) * i - 25)
                WIN.blit(text, textRect)

    pygame.display.flip()

    pygame.display.update()


def check_valid(row, col, num):
    for i in range(0, 9):
        if board[row][i] == num:
            return False
        if board[i][col] == num:
            return False
    row_block = row // 3
    col_block = col // 3
    row_range = [row_block * 3, row_block * 3 + 1, row_block * 3 + 2]
    col_range = [col_block * 3, col_block * 3 + 1, col_block * 3 + 2]
    for i in row_range:
        for j in col_range:
            if board[i][j] == num:
                return False
    return True


def userClick(pos, num):
    x, y = pos
    for i in range(0, 9):
        if i * 50 < x < (i + 1) * 50:
            col = i
        if i * 50 < y < (i + 1) * 50:
            row = i
    if board[row][col] == 0 and check_valid(row, col, num):
        board[row][col] = num


def draw_XO():
    pygame.display.update()


def reset_game():
    pass


def check_win():
    for row in range(0, 9):
        for col in range(0, 9):
            if board[row][col] == 0:
                return False
    return True


def check_click(event, pos):
    if event.key == pygame.K_1:
        userClick(pos, 1)
    elif event.key == pygame.K_2:
        userClick(pos, 2)
    elif event.key == pygame.K_3:
        userClick(pos, 3)
    elif event.key == pygame.K_4:
        userClick(pos, 4)
    elif event.key == pygame.K_5:
        userClick(pos, 5)
    elif event.key == pygame.K_6:
        userClick(pos, 6)
    elif event.key == pygame.K_7:
        userClick(pos, 7)
    elif event.key == pygame.K_8:
        userClick(pos, 8)
    elif event.key == pygame.K_9:
        userClick(pos, 9)


def find_empty():
    for row in range(0, 9):
        for col in range(0, 9):
            if board[row][col] == 0:
                return row, col
    return None


def solve():
    find = find_empty()
    if find == None:
        return True
    else:
        for num in range(1, 10):
            if check_valid(find[0], find[1], num):
                board[find[0]][find[1]] = num
                if solve() == True:
                    return True

            board[find[0]][find[1]] = 0
        return False


def undo(pos):
    x, y = pos
    for i in range(0, 9):
        if x > i * 50 and x < (i + 1) * 50:
            col = i
        if y > i * 50 and y < (i + 1) * 50:
            row = i
    board[row][col] = 0


def main():
    fill_board()
    clock = pygame.time.Clock()
    pygame.display.set_caption("First game!")
    run = True
    pos = 0, 0
    clicked = False
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    clicked = True
                if event.button == 3:
                    undo(pygame.mouse.get_pos())

            if event.type == pygame.KEYDOWN and clicked == True:
                check_click(event, pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    solve()

            draw_window()

            if check_win():
                pygame.display.flip()
                pygame.display.update()
                reset_game()
    pygame.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
