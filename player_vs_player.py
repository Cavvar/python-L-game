#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------*-------  Import Statements -------*------- #
import pygame
import sys
# -------*------- Global Constant Variables -------*------- #
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
CHOCOLATE = (210, 105, 30)
PURPLE = (191, 62, 255)
DARKPURPLE = (154, 50, 205)
GREEN = (0, 139, 0)
DARKGREEN = (0, 100, 0)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 610
BLOCK_WIDTH = 150
BLOCK_HEIGHT = 150
MARGIN = 2

FPS = 60

GRID_SIZE_Y = 4
GRID_SIZE_X = 4

L_PATTERN_ONE = [[0, 1], [0, 2], [0, 3], [1, 3]]
L_PATTERN_TWO = [[1, 1], [1, 2], [1, 3], [0, 3]]
L_PATTERN_THREE = [[0, 3], [0, 2], [0, 1], [1, 1]]
L_PATTERN_FOUR = [[0, 1], [1, 1], [1, 2], [1, 3]]
L_PATTERN_FIVE = [[0, 2], [0, 3], [1, 3], [2, 3]]
L_PATTERN_SIX = [[2, 2], [2, 3], [1, 3], [0, 3]]
L_PATTERN_SEVEN = [[0, 2], [1, 2], [2, 2], [2, 3]]
L_PATTERN_EIGHT = [[2, 2], [1, 2], [0, 2], [0, 3]]

# -------*------- Code Implementation -------*------- #


class Board(pygame.sprite.Sprite):

    def __init__(self, block_type):
        pygame.sprite.Sprite.__init__(self)
        self.block_type = block_type

        if block_type == 2:  # Playing Grid
            self.image = pygame.image.load("basic_block2.gif").convert()

        self.rect = self.image.get_rect()

    def transform(self, block_type):
        self.block_type = block_type

        if block_type == 1:  # Red L
            self.image = pygame.image.load("basic_block1.gif").convert()
        elif block_type == 2:  # Playing Grid
            self.image = pygame.image.load("basic_block2.gif").convert()
        elif block_type == 3:  # Blue L
            self.image = pygame.image.load("basic_block3.gif").convert()
        elif block_type == 4:
            self.image = pygame.image.load("basic_block4.gif").convert()
        elif block_type == 5:  # Green Circle
            self.image = pygame.image.load("basic_block5.gif").convert()
        elif block_type == 6:  # Purple Circle
            self.image = pygame.image.load("basic_block6.gif").convert()


class Game(object):
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.clock = pygame.time.Clock()

        self.background = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.background.fill(GRAY)

        pygame.display.flip()

        self.sprites = pygame.sprite.RenderUpdates()
        self.sprites_to_update = pygame.sprite.RenderUpdates()

        self.block_grid = [[Board(2) for y in range(GRID_SIZE_Y)] for x in range(GRID_SIZE_X)]
        for i in range(GRID_SIZE_X):
            for j in range(GRID_SIZE_Y):
                self.block_grid[i][j].rect.topleft = (MARGIN + BLOCK_WIDTH) * i + MARGIN, \
                                                     (MARGIN + BLOCK_HEIGHT) * j + MARGIN
                self.block_grid[i][j].indexes = i, j
                self.sprites.add(self.block_grid[i][j])

        self.which_piece_to_move = 1  # 1 Red-Piece-Moving, 2 Blue-Piece-Moving
        self.move_circle_or_not = False
        self.which_circle_to_move = 0  # Circle One (Top left), Circle Two (Bottom Right) , 3 not moving

        self.red_piece = []
        self.blue_piece = []
        self.green_circle = []
        self.purple_circle = []
        self.moving_blue_piece = []
        self.moving_red_piece = []
        self.help_message = "Red Player's turn"
        self.help_message_circle = ""
        self.ongoing_move_message = ""

    def set_red_piece(self):
        self.red_piece.append([1, 1])
        self.red_piece.append([1, 2])
        self.red_piece.append([1, 3])
        self.red_piece.append([2, 3])
        self.rearrange_grid(self.red_piece, 1)

    def set_blue_piece(self):
        self.blue_piece.append([1, 0])
        self.blue_piece.append([2, 0])
        self.blue_piece.append([2, 1])
        self.blue_piece.append([2, 2])
        self.rearrange_grid(self.blue_piece, 3)

    def set_green_circle(self):
        self.green_circle.append([0, 0])
        self.rearrange_grid(self.green_circle, 5)

    def set_purple_circle(self):
        self.purple_circle.append([3, 3])
        self.rearrange_grid(self.purple_circle, 6)

    def move_blue_piece(self, x, y):
        if len(self.moving_blue_piece) == 0:
            self.ongoing_move_message = ""
        if len(self.moving_blue_piece) <= 4 and \
                (self.block_grid[x][y].block_type == 2 or self.block_grid[x][y].block_type == 3):
            self.moving_blue_piece.append([x, y])
            if self.help_message != "Player Blue has lost the game":
                self.ongoing_move_message += str([x, y]) + " "
            if len(self.moving_blue_piece) == 4:
                if self.check_form_of_l(self.moving_blue_piece) and \
                                sorted(self.moving_blue_piece) != sorted(self.blue_piece):
                    self.rearrange_grid(self.blue_piece, 2)
                    self.rearrange_grid(self.moving_blue_piece, 3)
                    self.blue_piece = self.moving_blue_piece+[]
                    self.display_frame()
                    self.moving_blue_piece = []
                    self.which_piece_to_move = 1
                    self.help_message_circle = "Decide which circle you want to move"
                    self.move_circle_or_not = True
                    self.which_circle_to_move = 0
                else:
                    if self.help_message != "Player Blue has lost the game":
                        self.ongoing_move_message = "Invalid Move"
                    self.moving_blue_piece = []

    def move_red_piece(self, x, y):
        if len(self.moving_red_piece) == 0:
            self.ongoing_move_message = ""
        if len(self.moving_red_piece) <= 4 and \
                (self.block_grid[x][y].block_type == 2 or self.block_grid[x][y].block_type == 1):
            self.moving_red_piece.append([x, y])
            if self.help_message != "Player Red has lost the game":
                self.ongoing_move_message += str([x, y]) + " "
            if len(self.moving_red_piece) == 4:
                if self.check_form_of_l(self.moving_red_piece) \
                        and sorted(self.moving_red_piece) != sorted(self.red_piece):
                    self.rearrange_grid(self.red_piece, 2)
                    self.rearrange_grid(self.moving_red_piece, 1)
                    self.red_piece = self.moving_red_piece+[]
                    self.display_frame()
                    self.moving_red_piece = []
                    self.which_piece_to_move = 2
                    self.help_message_circle = "Decide which circle you want to move"
                    self.move_circle_or_not = True
                    self.which_circle_to_move = 0
                else:
                    if self.help_message != "Player Red has lost the game":
                        self.ongoing_move_message = "Invalid Move"
                    self.moving_red_piece = []

    @staticmethod
    def move_to_bottom_left(l_piece):
        temp_piece = []
        temp_piece_two = []
        temp_piece_three = []
        temp_piece_four = []

        for index in l_piece:
            if index[1]+1 <= GRID_SIZE_Y-1 and len(temp_piece) < 4:  # Movement down
                temp_piece.append([index[0], index[1]+1])
            if index[1]+1 == 4:
                temp_piece = l_piece

        for index in temp_piece:  # Movement to the left
            if index[0]-1 >= 0 and len(temp_piece_two) < 4:
                temp_piece_two.append([index[0]-1, index[1]])
            if index[0]-1 == -1:
                temp_piece_two = temp_piece

        for index in temp_piece_two:
            if index[1]+1 <= GRID_SIZE_Y-1 and len(temp_piece_three) < 4:  # Movement down
                temp_piece_three.append([index[0], index[1]+1])
            if index[1]+1 == 4:
                temp_piece_three = temp_piece_two

        for index in temp_piece_three:  # Movement to the left
            if index[0]-1 >= 0 and len(temp_piece_four) < 4:
                temp_piece_four.append([index[0]-1, index[1]])
            if index[0]-1 == -1:
                temp_piece_four = temp_piece_three

        return temp_piece_four

    def check_form_of_l(self, l_piece_to_check):
        temp_piece = self.move_to_bottom_left(l_piece_to_check)

        if sorted(temp_piece) == sorted(L_PATTERN_ONE) or sorted(temp_piece) == sorted(L_PATTERN_TWO) or  \
                sorted(temp_piece) == sorted(L_PATTERN_THREE) or \
                sorted(temp_piece) == sorted(L_PATTERN_FOUR) or \
                sorted(temp_piece) == sorted(L_PATTERN_FIVE) or \
                sorted(temp_piece) == sorted(L_PATTERN_SIX) or \
                sorted(temp_piece) == sorted(L_PATTERN_SEVEN) \
                or sorted(temp_piece) == sorted(L_PATTERN_EIGHT):

            return True
        else:
            return False

    def check_if_lost_and_whose_turn_it_is(self):
        if self.which_piece_to_move == 1:
            if len(self.get_available_moves(self.red_piece)) == 0:
                self.help_message = "Player Red has lost the game"
            elif len(self.get_available_moves(self.red_piece)) != 0 and self.move_circle_or_not is False:
                self.help_message = "Red Player's turn"
        elif self.which_piece_to_move == 2:
            if len(self.get_available_moves(self.blue_piece)) == 0:
                self.help_message = "Player Blue has lost the game"
            elif len(self.get_available_moves(self.blue_piece)) != 0 and self.move_circle_or_not is False:
                self.help_message = "Blue Player's turn"

    def move_green_circle(self, x, y):
        temp_piece = []
        if self.block_grid[x][y].block_type == 2:
            temp_piece.append([x, y])
            self.rearrange_grid(self.green_circle, 2)
            self.rearrange_grid(temp_piece, 5)
            self.green_circle = temp_piece+[]
            self.display_frame()
            self.move_circle_or_not = False
        else:
            self.help_message = "Invalid Move"
        self.check_if_lost_and_whose_turn_it_is()
        self.help_message_circle = ""
        self.ongoing_move_message = ""

    def move_purple_circle(self, x, y):
        temp_piece = []
        if self.block_grid[x][y].block_type == 2:
            temp_piece.append([x, y])
            self.rearrange_grid(self.purple_circle, 2)
            self.rearrange_grid(temp_piece, 6)
            self.purple_circle = temp_piece+[]
            self.display_frame()
            self.move_circle_or_not = False
        else:
            self.help_message = "Invalid Move"
        self.check_if_lost_and_whose_turn_it_is()
        self.help_message_circle = ""
        self.ongoing_move_message = ""

    def rearrange_grid(self, trans_object, block_type):
        for index in trans_object:
            self.block_grid[index[0]][index[1]].transform(block_type)

    def check_l_position(self, l_piece):
        amount_of_equal_cells = 0
        occupied_fields = []
        for x in range(4):
            for y in range(4):
                if self.which_piece_to_move == 1:
                    if self.block_grid[x][y].block_type != 2 and self.block_grid[x][y].block_type != 1:
                        occupied_fields.append([x, y])
                elif self.which_piece_to_move == 2:
                    if self.block_grid[x][y].block_type != 2 and self.block_grid[x][y].block_type != 3:
                        occupied_fields.append([x, y])

        for index_one in occupied_fields:
            for index_two in l_piece:
                if index_one[0] == index_two[0] and index_one[1] == index_two[1]:
                    amount_of_equal_cells += 1

        if amount_of_equal_cells == 0:
            return True

    def get_available_moves(self, which_piece_to_check):
        possible_moves_list = self.move_piece_around_the_board(L_PATTERN_ONE, which_piece_to_check) + \
              self.move_piece_around_the_board(L_PATTERN_TWO, which_piece_to_check) + \
              self.move_piece_around_the_board(L_PATTERN_THREE, which_piece_to_check) + \
              self.move_piece_around_the_board(L_PATTERN_FOUR, which_piece_to_check) + \
              self.move_piece_around_the_board(L_PATTERN_FIVE, which_piece_to_check) + \
              self.move_piece_around_the_board(L_PATTERN_SIX, which_piece_to_check) + \
              self.move_piece_around_the_board(L_PATTERN_SEVEN, which_piece_to_check) + \
              self.move_piece_around_the_board(L_PATTERN_EIGHT, which_piece_to_check)
        return possible_moves_list

    def move_piece_around_the_board(self, lpiece, which_piece_to_check):
        temp_piece = lpiece
        temp_piece_two = []
        possible_moves_list = []
        amount_of_possible_moves = 0

        for to_right in range(2):
            for index in temp_piece:
                if index[0]+1 <= GRID_SIZE_X-1 and len(temp_piece_two) < 4:
                    temp_piece_two.append([index[0]+1, index[1]])
            if len(temp_piece_two) < 4:
                temp_piece_two = temp_piece
            if len(temp_piece_two) == 4:
                if self.check_l_position(temp_piece_two) and sorted(temp_piece_two) != sorted(which_piece_to_check) \
                        and sorted(temp_piece) != sorted(temp_piece_two):
                    amount_of_possible_moves += 1
                    possible_moves_list.append(temp_piece_two)
                temp_piece = temp_piece_two
                temp_piece_two = []

        for to_top in range(2):
            for index in temp_piece:
                if index[1]-1 >= 0 and len(temp_piece_two) < 4:
                    temp_piece_two.append([index[0], index[1]-1])
            if len(temp_piece_two) < 4:
                temp_piece_two = temp_piece
            if len(temp_piece_two) == 4:
                if self.check_l_position(temp_piece_two) and sorted(temp_piece_two) != sorted(which_piece_to_check) \
                        and sorted(temp_piece) != sorted(temp_piece_two):
                    amount_of_possible_moves += 1
                    possible_moves_list.append(temp_piece_two)
                temp_piece = temp_piece_two
                temp_piece_two = []

        for to_left in range(2):
            for index in temp_piece:
                if index[0]-1 >= 0 and len(temp_piece_two) < 4:
                    temp_piece_two.append([index[0]-1, index[1]])
            if len(temp_piece_two) < 4:
                temp_piece_two = temp_piece
            if len(temp_piece_two) == 4:
                if self.check_l_position(temp_piece_two) and sorted(temp_piece_two) != sorted(which_piece_to_check) \
                        and sorted(temp_piece) != sorted(temp_piece_two):
                    amount_of_possible_moves += 1
                    possible_moves_list.append(temp_piece_two)
                temp_piece = temp_piece_two
                temp_piece_two = []

        for to_bottom in range(2):
            for index in temp_piece:
                if index[1]+1 <= GRID_SIZE_Y-1 and len(temp_piece_two) < 4:
                    temp_piece_two.append([index[0], index[1]+1])
            if len(temp_piece_two) < 4:
                temp_piece_two = temp_piece
            if len(temp_piece_two) == 4:
                if self.check_l_position(temp_piece_two) and sorted(temp_piece_two) != sorted(which_piece_to_check) \
                        and sorted(temp_piece) != sorted(temp_piece_two):
                    amount_of_possible_moves += 1
                    possible_moves_list.append(temp_piece_two)
                temp_piece = temp_piece_two
                temp_piece_two = []

        return possible_moves_list

    def handle_events(self):
        pos = pygame.mouse.get_pos()

        column = pos[0] // (BLOCK_WIDTH + MARGIN)
        row = pos[1] // (BLOCK_HEIGHT + MARGIN)

        events = pygame.event.get()
        try:
            for event in events:
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.move_circle_or_not:
                    if self.which_piece_to_move == 1:
                        self.move_red_piece(column, row)
                    elif self.which_piece_to_move == 2:
                        self.move_blue_piece(column, row)
                elif event.type == pygame.MOUSEBUTTONDOWN and self.move_circle_or_not:
                    if self.which_circle_to_move == 1:
                        self.move_green_circle(column, row)
                    elif self.which_circle_to_move == 2:
                        self.move_purple_circle(column, row)

        except IndexError:
            pass

        return True

    @staticmethod
    def text_objects(text, font):
        text_surface = font.render(text, True, BLACK)
        return text_surface, text_surface.get_rect()

    # msg: Text der auf dem Knopf steht - x: Position auf der x-Achse - y: Position auf der y-Achse
    # w: Breite des Knopfes - h: Höhe des Knopfes - ic: Farbe des Knopfes
    # ac: Farbe des Knopfes während die Maus darüber steht - action: Aktion, die beim Betätigen des Knopfes passiert
    def button(self, msg, x, y, w, h, ic, ac, action):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(self.window, ac, (x, y, w, h))
            if click[0] == 1 and action is not None:
                if action == "Move Green Circle":
                    self.which_circle_to_move = 1
                elif action == "Move Purple Circle":
                    self.which_circle_to_move = 2
                elif action == "Not Moving":
                    self.check_if_lost_and_whose_turn_it_is()
                    self.help_message_circle = ""
                    self.ongoing_move_message = ""
                    self.move_circle_or_not = False

        else:
            pygame.draw.rect(self.window, ic, (x, y, w, h))

        small_text = pygame.font.Font("freesansbold.ttf", 20)
        text_surf, text_rect = self.text_objects(msg, small_text)
        text_rect.center = ((x+(w/2)), (y+(h/2)))
        self.window.blit(text_surf, text_rect)

    def display_help_to_screen(self, msg, x, y):
        small_text = pygame.font.Font("freesansbold.ttf", 18)
        text_surf, text_rect = self.text_objects(msg, small_text)
        text_rect.centerx = x
        text_rect.centery = y
        self.window.blit(text_surf, text_rect)

    def display_frame(self):
        for sprite in self.sprites_to_update:
            sprite.update()

        self.sprites.draw(self.background)
        self.window.blit(self.background, (0, 0))

        self.button("Green", 620, 127, 100, 50, GREEN, DARKGREEN, "Move Green Circle")
        self.button("Purple", 620, 280, 100, 50, PURPLE, DARKPURPLE, "Move Purple Circle")
        self.button("No Circle", 620, 432, 100, 50, WHITE, CHOCOLATE, "Not Moving")

        self.display_help_to_screen(self.help_message, 860, 305)
        self.display_help_to_screen(self.help_message_circle, 806, 229)
        self.display_help_to_screen(self.ongoing_move_message, 806, 384)

        pygame.display.flip()

    def run(self):
        print 'Starting Event Loop'
        running = True

        self.set_red_piece()
        self.set_blue_piece()
        self.set_purple_circle()
        self.set_green_circle()

        while running:
            self.clock.tick(FPS)
            self.display_frame()
            running = self.handle_events()

        print 'Quitting. Thanks for playing'
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
