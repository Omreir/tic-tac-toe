"""
Project: Tic-Tac-Toe
Description: This program is a simple tic-tac-toe game. There are three game modes; "pvp" (player vs player),
             "pvr" (player vs robot, "rvr" (robot vs robot). "rvr" mode only plays 3 games. Initially starts on "pvp".
Author: Riley Morrison
Date: 8/02/2025
"""
import pygame
import random


# Scoreboard class keeps track of the score.
class Scoreboard:

    # Initiates the default values.
    def __init__(self):
        self.x_score = 0
        self.o_score = 0
        self.draw = 0

    # add_score method adds one points to the symbol put in the parameter. Can only be x or o.
    def add_score(self, symbol):

        # Checks what symbol is in the parameter and adds one to their score.
        if symbol == "x":
            self.x_score += 1

        elif symbol == "o":
            self.o_score += 1

        elif symbol == "d":
            self.draw += 1

    # get_x_score method returns the x player's score.
    def get_x_score(self):
        return self.x_score

    # get_o_score method returns the o player's score.
    def get_o_score(self):
        return self.o_score

    # Returns a readable version of the score if class is printed.
    def __str__(self):
        return (f"X : {self.x_score}"
                f"O : {self.o_score}")

    # reset method resets the players scores.
    def reset(self):
        print("Score Reset")
        self.o_score = 0
        self.x_score = 0
        self.draw = 0


# Board class keeps track of moves done and checks if there is a win, and if so gives it to the Scoreboard class.
class Board:

    # Initiates the defaults values and the defaults scoreboard object being used.
    def __init__(self, points):
        self.moves = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
        self.total_moves = 0
        self.total_games = 0
        self.points = points
        self.mode = "pvp"
        self.mode_hover = "none"
        self.reset_hover = "none"
        self.current_symbol = "x"
        self.possible_moves = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # new_move method records a move and takes it out of the possible moves list. Swaps what players turn it is.
    def new_move(self, move, symbol):
        self.moves[move - 1] = symbol
        self.possible_moves.remove(move)
        self.total_moves += 1
        self.check_win()

        match self.current_symbol:

            case "x":
                self.current_symbol = "o"

            case "o":
                self.current_symbol = "x"

    # Returns a readable version of the board if the method is printed.
    def __str__(self):
        return (f"| {self.moves[0]} | {self.moves[1]} | {self.moves[2]} |"
                f"\n- - - - - - -"
                f"\n| {self.moves[3]} | {self.moves[4]} | {self.moves[5]} |"
                f"\n- - - - - - -"
                f"\n| {self.moves[6]} | {self.moves[7]} | {self.moves[8]} |")

    # get_moves method returns a list that represents the board to show what piece is where.
    def get_moves(self):
        return self.moves

    # reset method makes the board empty, resetting back to the default values. This does not change the score.
    def reset(self):
        self.moves = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
        self.possible_moves = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.total_moves = 0

    # new_game method does the same as the reset method, but it resets the score as well.
    def new_game(self):
        self.reset()
        self.points.reset()

    # win method updates the score and gets it ready for a new game.
    # Also keeps track of the total games when in "rvr" mode, so it can reset after 3 games.
    # Allows three symbols 'x', 'o' and 'd' (draw).
    def win(self, symbol):
        pygame.time.wait(1000)
        self.reset()
        self.points.add_score(symbol)

        if self.mode == "rvr":
            self.total_games += 1

        # Goes to menu after three games in "rvr", so there isn't an infinite loop.
        if self.total_games == 3:
            self.mode = "menu"
            self.total_games = 0
            self.mode_hover = "none"
            self.reset()

    # check_win method checks if any player has won, and if so calls the win method, also checks if it is a draw.
    # Note that this method doesn't check pre-defined conditions, but independently checks for a win.
    def check_win(self):

        # Checks for a horizontal win.
        for column in range(3):
            total_symbol = 0

            for row in range(3):

                if self.moves[(column * 3) + row] == self.current_symbol:
                    total_symbol += 1

            if total_symbol == 3:
                print("Horizontal Win!")
                self.win(self.current_symbol)

        # Checks for a vertical win.
        for row in range(3):
            total_symbol = 0

            for column in range(3):

                if self.moves[(column * 3) + row] == self.current_symbol:
                    total_symbol += 1

            if total_symbol == 3:
                print("Vertical Win!")
                self.win(self.current_symbol)

        # Checks for a diagonal win.
        for diagonal in range(2):
            total_symbol = 0

            for intercept in range(3):

                if (diagonal * 2) == 0:

                    if self.moves[intercept * 4] == self.current_symbol:
                        total_symbol += 1

                else:

                    if self.moves[(diagonal * 2) + (intercept * 2)] == self.current_symbol:
                        total_symbol += 1

            if total_symbol == 3:
                print("Diagonal Win!")
                self.win(self.current_symbol)

        # Calls win if it is a draw.
        if self.total_moves == 9:
            self.win("d")


# Class creates the user interface and has methods that make it work.
class BoardUI:

    # Initiates the UI. Changes the screen size to fit the monitor.
    def __init__(self, board, points):
        self.board = board
        self.offset = 1

        # This loop changes the screen size offset which is used by everything seen on the screen.
        while (1000 / self.offset) >= pygame.display.Info().current_h:
            self.offset += 1

        self.screen = pygame.display.set_mode([1000 / self.offset, 1000 / self.offset])
        pygame.display.set_caption("Tic-Tac-Toe")
        self.text_size = 60 / self.offset
        self.text_font = pygame.font.SysFont("Arial", int(self.text_size))
        self.points = points
        # position_values list stores the location of each place that can have a piece placed on it.
        self.position_values = [[0, 0], [300, 0], [600, 0], [0, 300], [300, 300], [600, 300], [0, 600], [300, 600], [600, 600]]

    # write_text method allows text to be written at the specified location.
    def write_text(self, text, font, text_colour, width, height):
        writing = font.render(text, True, text_colour)
        self.screen.blit(writing, (width, height))

    # Loads the board and symbols again, so the symbols are updated.
    def load_symbols(self):
        self.draw_board()
        x_points = self.points.x_score
        o_points = self.points.o_score
        draw = self.points.draw

        # Creates the scoreboard, so you can tell the score.
        match board1.current_symbol:

            case "x":
                self.write_text(f"x : {x_points}", self.text_font, "orange", 110 / self.offset, 915 / self.offset)
                self.write_text(f"o : {o_points}", self.text_font, "white", 410 / self.offset, 915 / self.offset)

            case "o":
                self.write_text(f"x : {x_points}", self.text_font, "white", 110 / self.offset, 915 / self.offset)
                self.write_text(f"o : {o_points}", self.text_font, "hotpink2", 410 / self.offset, 915 / self.offset)

        self.write_text(f"d : {draw}", self.text_font, "white", 710 / self.offset, 915 / self.offset)
        moves = self.board.get_moves()
        x_moves = []
        o_moves = []
        number = 0

        # Converts the values from moves list to know the location of each move and who did it.
        for spot in moves:

            if spot == "x":
                x_moves.append(number)

            elif spot == "o":
                o_moves.append(number)

            number += 1

        # Puts the player symbols on the board at each location placed.
        for spot in x_moves:
            self.place(False, "x", spot)

        for spot in o_moves:
            self.place(False, "o", spot)

    # Makes the board without symbols, except for the mode buttons, because it does not change except for colour.
    def draw_board(self):
        self.screen.fill("dodgerblue")
        pygame.draw.rect(self.screen, "dodgerblue4", (0, 900 / self.offset, 900 / self.offset, 100 / self.offset))
        pygame.draw.rect(self.screen, "deepskyblue4", (900 / self.offset, 900 / self.offset, 100 / self.offset, 100 / self.offset))

        # Makes the reset button change colour when your cursor is hovering over it.
        if self.board.reset_hover == "reset":
            pygame.draw.rect(self.screen, "brown4", (900 / self.offset, 900 / self.offset, 100 / self.offset, 100 / self.offset))

        # Makes the modes buttons change colour when your cursor is hovering over it.
        match self.board.mode_hover:

            case "none":
                pygame.draw.rect(self.screen, "dodgerblue3", (900 / self.offset, 0, 100 / self.offset, 300 / self.offset))
                pygame.draw.rect(self.screen, "dodgerblue3", (900 / self.offset, 300 / self.offset, 100 / self.offset, 300 / self.offset))
                pygame.draw.rect(self.screen, "dodgerblue3", (900 / self.offset, 600 / self.offset, 100 / self.offset, 300 / self.offset))

            case "pvp":
                pygame.draw.rect(self.screen, "deepskyblue3", (900 / self.offset, 0, 100 / self.offset, 300 / self.offset))
                pygame.draw.rect(self.screen, "dodgerblue3", (900 / self.offset, 300 / self.offset, 100 / self.offset, 300 / self.offset))
                pygame.draw.rect(self.screen, "dodgerblue3", (900 / self.offset, 600 / self.offset, 100 / self.offset, 300 / self.offset))

            case "pvr":
                pygame.draw.rect(self.screen, "dodgerblue3", (900 / self.offset, 0, 100 / self.offset, 300 / self.offset))
                pygame.draw.rect(self.screen, "deepskyblue3", (900 / self.offset, 300 / self.offset, 100 / self.offset, 300 / self.offset))
                pygame.draw.rect(self.screen, "dodgerblue3", (900 / self.offset, 600 / self.offset, 100 / self.offset, 300 / self.offset))

            case "rvr":
                pygame.draw.rect(self.screen, "dodgerblue3", (900 / self.offset, 0, 100 / self.offset, 300 / self.offset))
                pygame.draw.rect(self.screen, "dodgerblue3", (900 / self.offset, 300 / self.offset, 100 / self.offset, 300 / self.offset))
                pygame.draw.rect(self.screen, "deepskyblue3", (900 / self.offset, 600 / self.offset, 100 / self.offset, 300 / self.offset))

        # Makes the modes button change colour when the mode is selected.
        match self.board.mode:

            case "pvp":
                pygame.draw.rect(self.screen, "dodgerblue4", (900 / self.offset, 0, 100 / self.offset, 300 / self.offset))
                self.write_text("p", self.text_font, "green", 940 / self.offset, 45 / self.offset)
                self.write_text("v", self.text_font, "green", 940 / self.offset, 95 / self.offset)
                self.write_text("p", self.text_font, "green", 940 / self.offset, 145 / self.offset)
                self.write_text("p", self.text_font, "white", 940 / self.offset, 345 / self.offset)
                self.write_text("v", self.text_font, "white", 940 / self.offset, 395 / self.offset)
                self.write_text("r", self.text_font, "white", 940 / self.offset, 445 / self.offset)
                self.write_text("r", self.text_font, "white", 940 / self.offset, 645 / self.offset)
                self.write_text("v", self.text_font, "white", 940 / self.offset, 695 / self.offset)
                self.write_text("r", self.text_font, "white", 940 / self.offset, 745 / self.offset)

            case "pvr":
                pygame.draw.rect(self.screen, "dodgerblue4", (900 / self.offset, 300 / self.offset, 100 / self.offset, 300 / self.offset))
                self.write_text("p", self.text_font, "white", 940 / self.offset, 45 / self.offset)
                self.write_text("v", self.text_font, "white", 940 / self.offset, 95 / self.offset)
                self.write_text("p", self.text_font, "white", 940 / self.offset, 145 / self.offset)
                self.write_text("p", self.text_font, "green", 940 / self.offset, 345 / self.offset)
                self.write_text("v", self.text_font, "green", 940 / self.offset, 395 / self.offset)
                self.write_text("r", self.text_font, "green", 940 / self.offset, 445 / self.offset)
                self.write_text("r", self.text_font, "white", 940 / self.offset, 645 / self.offset)
                self.write_text("v", self.text_font, "white", 940 / self.offset, 695 / self.offset)
                self.write_text("r", self.text_font, "white", 940 / self.offset, 745 / self.offset)

            case "rvr":
                pygame.draw.rect(self.screen, "dodgerblue4", (900 / self.offset, 600 / self.offset, 100 / self.offset, 300 / self.offset))
                self.write_text("p", self.text_font, "white", 940 / self.offset, 45 / self.offset)
                self.write_text("v", self.text_font, "white", 940 / self.offset, 95 / self.offset)
                self.write_text("p", self.text_font, "white", 940 / self.offset, 145 / self.offset)
                self.write_text("p", self.text_font, "white", 940 / self.offset, 345 / self.offset)
                self.write_text("v", self.text_font, "white", 940 / self.offset, 395 / self.offset)
                self.write_text("r", self.text_font, "white", 940 / self.offset, 445 / self.offset)
                self.write_text("r", self.text_font, "green", 940 / self.offset, 645 / self.offset)
                self.write_text("v", self.text_font, "green", 940 / self.offset, 695 / self.offset)
                self.write_text("r", self.text_font, "green", 940 / self.offset, 745 / self.offset)

            case "menu":
                self.write_text("p", self.text_font, "white", 940 / self.offset, 45 / self.offset)
                self.write_text("v", self.text_font, "white", 940 / self.offset, 95 / self.offset)
                self.write_text("p", self.text_font, "white", 940 / self.offset, 145 / self.offset)
                self.write_text("p", self.text_font, "white", 940 / self.offset, 345 / self.offset)
                self.write_text("v", self.text_font, "white", 940 / self.offset, 395 / self.offset)
                self.write_text("r", self.text_font, "white", 940 / self.offset, 445 / self.offset)
                self.write_text("r", self.text_font, "white", 940 / self.offset, 645 / self.offset)
                self.write_text("v", self.text_font, "white", 940 / self.offset, 695 / self.offset)
                self.write_text("r", self.text_font, "white", 940 / self.offset, 745 / self.offset)

        # Creates the lines on the board.
        pygame.draw.line(self.screen, "white", (300 / self.offset, 0), (300 / self.offset, 1000 / self.offset), 5)
        pygame.draw.line(self.screen, "white", (600 / self.offset, 0), (600 / self.offset, 1000 / self.offset), 5)
        pygame.draw.line(self.screen, "white", (0, 300 / self.offset), (1000 / self.offset, 300 / self.offset), 5)
        pygame.draw.line(self.screen, "white", (0, 600 / self.offset), (1000 / self.offset, 600 / self.offset), 5)
        pygame.draw.line(self.screen, "white", (0, 900 / self.offset), (1000 / self.offset, 900 / self.offset), 5)
        pygame.draw.line(self.screen, "white", (900 / self.offset, 0), (900 / self.offset, 1000 / self.offset), 5)
        pygame.draw.line(self.screen, "white", (0, 0), (0, 1000 / self.offset), 5)
        pygame.draw.line(self.screen, "white", (0, 0), (1000 / self.offset, 0), 5)
        pygame.draw.line(self.screen, "white", (0, 1000 / self.offset), (1000 / self.offset, 1000 / self.offset), 5)
        pygame.draw.line(self.screen, "white", (1000 / self.offset, 0), (1000 / self.offset, 1000 / self.offset), 5)
        pygame.draw.line(self.screen, "red", (925 / self.offset, 925 / self.offset), (975 / self.offset, 975 / self.offset), 5)
        pygame.draw.line(self.screen, "red", (975 / self.offset, 925 / self.offset), (925 / self.offset, 975 / self.offset), 5)

    # place method places a symbol on the board and is used by other methods to do this.
    def place(self, hover, symbol, square):
        # offsets are needed to make the symbols be placed on a set location.
        x_offset = self.position_values[square][0] / self.offset
        y_offset = self.position_values[square][1] / self.offset

        # Changes the colour of the symbol depending on player and if they are hovering over it or not.
        if symbol == "x":

            if hover:
                colour = "white"

            else:
                colour = "orange"

            pygame.draw.line(self.screen, colour, (((110 / self.offset) + x_offset), ((110 / self.offset) + y_offset)), (((190 / self.offset) + x_offset), ((190 / self.offset) + y_offset)), int(10 / self.offset))
            pygame.draw.line(self.screen, colour, (((110 / self.offset) + x_offset), ((190 / self.offset) + y_offset)), (((190 / self.offset) + x_offset), ((110 / self.offset) + y_offset)), int(10 / self.offset))

        elif symbol == "o":

            if hover:
                colour = "white"

            else:
                colour = "hotpink2"

            pygame.draw.circle(self.screen, colour, (((150 / self.offset) + x_offset), ((150 / self.offset) + y_offset)), int(40 / self.offset))
            pygame.draw.circle(self.screen, "dodgerblue1", (((150 / self.offset) + x_offset), ((150 / self.offset) + y_offset)), int(25 / self.offset))


# Player class stores everything about the player and provides functionality.
class Player:

    # Initiates the player.
    def __init__(self, board, ui, symbol):
        self.board = board
        self.symbol = symbol
        self.boardUI = ui

    # opposite_symbol determines the opposite symbol of the given symbol in its parameter.
    def opposite_symbol(self, symbol):

        match symbol:

            case "x":
                opposite_symbol = "o"

            case "o":
                opposite_symbol = "x"

        return opposite_symbol

    # check_move is a static method that checks if the move is allowed by checking the board.
    def check_move(self, position):

        if board1.get_moves()[position - 1] == " ":
            return True

        else:
            return False

    # make_move method makes a move for the player and gives it to the board.
    def make_move(self, position):

        if self.check_move(position):
            self.board.new_move(position, self.symbol)

        else:
            print("Already taken")

    # random_move method makes a random move and was the original robot decision-making, taking into account the
    # possible moves.
    def random_move(self):
        position = random.choice(self.board.possible_moves)
        self.make_move(position)
        pygame.time.wait(500)

    # one_off_win method checks if the given player is one off of making a move and returns the position of that move.
    # This was a modified version of the check win method from the board class.
    def one_off_win(self, current_symbol):

        opposing_symbol = self.opposite_symbol(current_symbol)

        # Checks for a horizontal one off.
        for column in range(3):
            total_symbol = 0
            missing_symbol = []

            for row in range(3):

                if self.board.moves[(column * 3) + row] == current_symbol:
                    total_symbol += 1

                elif self.board.moves[(column * 3) + row] != opposing_symbol:
                    missing_symbol.append((column * 3) + row)

            if (total_symbol == 2) & (len(missing_symbol) > 0):
                return int(missing_symbol[0] + 1)

        # Checks for a vertical one off.
        for row in range(3):
            total_symbol = 0
            missing_symbol = []

            for column in range(3):

                if self.board.moves[(column * 3) + row] == current_symbol:
                    total_symbol += 1

                elif self.board.moves[(column * 3) + row] != opposing_symbol:
                    missing_symbol.append((column * 3) + row)

            if (total_symbol == 2) & (len(missing_symbol) > 0):
                return int(missing_symbol[0] + 1)

        # Checks for a diagonal one off.
        for diagonal in range(2):
            total_symbol = 0
            missing_symbol = []

            for intercept in range(3):

                if (diagonal * 2) == 0:

                    if self.board.moves[intercept * 4] == current_symbol:
                        total_symbol += 1

                    elif self.board.moves[intercept * 4] != opposing_symbol:
                        missing_symbol.append(intercept * 4)

                elif not ((diagonal * 2) == 0):

                    if self.board.moves[(diagonal * 2) + (intercept * 2)] == current_symbol:
                        total_symbol += 1

                    elif self.board.moves[(diagonal * 2) + (intercept * 2)] != opposing_symbol:
                        missing_symbol.append((diagonal * 2) + (intercept * 2))

            if (total_symbol == 2) & (len(missing_symbol) > 0):
                return int(missing_symbol[0] + 1)

        return 0

    # intelligent_move method is used by the robot to decide its move.
    def intelligent_move(self):
        opposing_symbol = self.opposite_symbol(self.symbol)
        attack_move = self.one_off_win(self.symbol)
        block_move = self.one_off_win(opposing_symbol)
        # Firstly checks if the middle square is empty, so it can take it first.
        if 5 in self.board.possible_moves:
            self.make_move(5)
            pygame.time.wait(500)

        # Secondly checks if it is one square off of a win and does so.
        elif attack_move != 0:

            if self.check_move(attack_move):
                self.make_move(attack_move)

        # Thirdly checks if the enemy is one square off of a win and does so.
        elif block_move != 0:
            if self.check_move(block_move):
                self.make_move(block_move)

        # If all the conditions above are not true it places a random move.
        else:
            self.random_move()

    # cursor method provides functionality to the cursor to know where it is hovering and clicking over.
    def cursor(self, position, hover):
        x_position = position[0]
        y_position = position[1]
        square = 0

        # If the mode is not "menu" it allows the user to click on any square.
        if self.board.mode != "menu":

            # Square 1
            if (x_position < 300 / self.boardUI.offset) & (x_position > 0) & (y_position < 300 / self.boardUI.offset) & (y_position > 0):
                square = 1

            # Square 2
            elif (x_position < 600 / self.boardUI.offset) & (x_position > 300 / self.boardUI.offset) & (y_position < 300 / self.boardUI.offset) & (y_position > 0):
                square = 2

            # Square 3
            elif (x_position < 900 / self.boardUI.offset) & (x_position > 600 / self.boardUI.offset) & (y_position < 300 / self.boardUI.offset) & (y_position > 0):
                square = 3

            # Square 4
            elif (x_position < 300 / self.boardUI.offset) & (x_position > 0) & (y_position < 600 / self.boardUI.offset) & (y_position > 300 / self.boardUI.offset):
                square = 4

            # Square 5
            elif (x_position < 600 / self.boardUI.offset) & (x_position > 300 / self.boardUI.offset) & (y_position < 600 / self.boardUI.offset) & (y_position > 300 / self.boardUI.offset):
                square = 5

            # Square 6
            elif (x_position < 900 / self.boardUI.offset) & (x_position > 600 / self.boardUI.offset) & (y_position < 600 / self.boardUI.offset) & (y_position > 300 / self.boardUI.offset):
                square = 6

            # Square 7
            elif (x_position < 300 / self.boardUI.offset) & (x_position > 0) & (y_position < 900 / self.boardUI.offset) & (y_position > 600 / self.boardUI.offset):
                square = 7

            # Square 8
            elif (x_position < 600 / self.boardUI.offset) & (x_position > 300 / self.boardUI.offset) & (y_position < 900 / self.boardUI.offset) & (y_position > 600 / self.boardUI.offset):
                square = 8

            # Square 9
            elif (x_position < 900 / self.boardUI.offset) & (x_position > 600 / self.boardUI.offset) & (y_position < 900 / self.boardUI.offset) & (y_position > 600 / self.boardUI.offset):
                square = 9

            # If cursor is hovering over a playable tile a cursor symbol is placed over it.
            if (square != 0) & hover & self.check_move(square):
                self.boardUI.place(hover, self.symbol, square - 1)

            # If it is a valid move it is placed.
            elif (square != 0) & self.check_move(square):
                self.board.new_move(square, self.symbol)

        # Checks if cursor is above the "pvp" mode button.
        if (x_position < 1000 / self.boardUI.offset) & (x_position > 900 / self.boardUI.offset) & (y_position < 300 / self.boardUI.offset) & (y_position > 0) & (self.board.mode != "pvp"):

            # Provides functionality if clicked.
            if not hover:
                self.board.points.reset()
                self.boardUI.draw_board()
                self.board.mode = "pvp"
                self.board.new_game()

            # Highlights the button if hovered over.
            else:
                self.board.mode_hover = "pvp"
                self.boardUI.draw_board()
                self.boardUI.load_symbols()

        # Checks if the cursor is above the "pvr" mode button.
        elif (x_position < 1000 / self.boardUI.offset) & (x_position > 900 / self.boardUI.offset) & (y_position < 600 / self.boardUI.offset) & (y_position > 300 / self.boardUI.offset) & (self.board.mode != "pvr"):

            # Provides functionality if clicked.
            if not hover:
                self.board.points.reset()
                self.boardUI.draw_board()
                self.board.mode = "pvr"
                self.board.new_game()
                self.boardUI.draw_board()
                self.boardUI.load_symbols()

            # Highlights the button if hovered over.
            else:
                self.board.mode_hover = "pvr"
                self.boardUI.draw_board()
                self.boardUI.load_symbols()

            # Stops highlighting the reset button.
            self.board.reset_hover = "none"

        # Checks if the cursor is above the "rvr" mode button.
        elif (x_position < 1000 / self.boardUI.offset) & (x_position > 900 / self.boardUI.offset) & (y_position < 900 / self.boardUI.offset) & (y_position > 600 / self.boardUI.offset) & (self.board.mode != "rvr"):

            # Provides functionality if clicked.
            if not hover:
                self.board.points.reset()
                self.boardUI.draw_board()
                self.board.mode = "rvr"
                self.board.new_game()
                self.boardUI.load_symbols()

            # Highlights the button if hovered over.
            else:
                self.board.mode_hover = "rvr"
                self.boardUI.draw_board()
                self.boardUI.load_symbols()

            # Stops highlighting the reset button.
            self.board.reset_hover = "none"

        # Checks if the cursor is above the reset button.
        elif (x_position < 1000 / self.boardUI.offset) & (x_position > 900 / self.boardUI.offset) & (y_position < 1000 / self.boardUI.offset) & (y_position > 900 / self.boardUI.offset):

            # Provides functionality if clicked.
            if not hover:
                self.board.points.reset()
                self.board.new_game()

            # Highlights the button if hovered over.
            else:
                self.board.reset_hover = "reset"
                self.boardUI.draw_board()
                self.boardUI.load_symbols()

            # If button is over the reset button it stops highlighting the mode buttons.
            self.board.mode_hover = "none"

        # If nothing is being hovered over the highlighting stops.
        else:
            self.board.mode_hover = "none"
            self.board.reset_hover = "none"


# Initiates the objects.
score = Scoreboard()
board1 = Board(score)
pygame.init()
interface = BoardUI(board1, score)
interface.draw_board()
interface.load_symbols()
running = True
x_player = Player(board1, interface, "x")
o_player = Player(board1, interface, "o")

# Every line in the loop is being done repeatedly until the exit button is clicked.
while running:

    # Checks if the exit button has been clicked.
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    interface.load_symbols()

    # Provides functionality if the game is in menu mode.
    if board1.mode == "menu":
        # Track the mouse to know what it is hovering over.
        x_player.cursor(pygame.mouse.get_pos(), True)

        # Provides functionality if mouse is clicked.
        if pygame.mouse.get_pressed()[0]:
            x_player.cursor(pygame.mouse.get_pos(), False)
            interface.draw_board()
            interface.load_symbols()

    # If the game is not in menu mode it provides functionality to the player to place pieces.
    else:

        # Gives the x player functionality when in "pvp" and "pvr" modes.
        if ((board1.mode == "pvp") | (board1.mode == "pvr")) & (board1.current_symbol == "x"):

            if board1.current_symbol == "x":
                # Tracks the mouse to know what it is hovering over.
                x_player.cursor(pygame.mouse.get_pos(), True)

                # Provides functionality if the mouse is clicked.
                if pygame.mouse.get_pressed()[0]:
                    x_player.cursor(pygame.mouse.get_pos(), False)
                    interface.draw_board()
                    interface.load_symbols()
                    pygame.time.wait(500)

        # If the mode is "rvr" or "pvr" the x player robot makes its move.
        elif (board1.mode == "rvr") & (board1.current_symbol == "x"):
            x_player.intelligent_move()
            pygame.time.wait(500)

        # Gives the o player functionality when in "pvp" mode.
        elif (board1.mode == "pvp") & (board1.current_symbol == "o"):
            # Tracks the mouse to know what it is hovering over.
            o_player.cursor(pygame.mouse.get_pos(), True)

            # Provides functionality if mouse is clicked.
            if pygame.mouse.get_pressed()[0]:
                o_player.cursor(pygame.mouse.get_pos(), False)
                interface.draw_board()
                interface.load_symbols()
                pygame.time.wait(500)

        # If the mode is "rvr" or "pvr" the o player robot makes its move.
        elif ((board1.mode == "pvr") | (board1.mode == "rvr")) & (board1.current_symbol == "o"):
            o_player.intelligent_move()
            pygame.time.wait(500)

    # Loads graphics.
    pygame.display.flip()

# If the exit button has been clicked the program terminates.
pygame.quit()
