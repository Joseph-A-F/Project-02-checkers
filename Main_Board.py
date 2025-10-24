"""
Main_Board.py
The Main_Board File holds the Main_Board class which is responsible for managing the board and the pieces.
"""

import pygame
from constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from pieces import Piece

class Main_Board:
    """
    The Main_Board class is responsible for managing the board and the pieces, and contains functions to draw the board, 
    evaluate the board, get all pieces, get a single piece, move a piece (left or right), create the board, draw the board, 
    remove a piece, and check for a winner.
    """
    def __init__(self, player_1_color, player_2_color, color):
        """
        The init function initializes the Main_Board class with a color and creates the board.
        """
        self.board = []
        self.color = color
        self.player_1_color = player_1_color
        self.player_2_color = player_2_color
        self.player_1_left = self.player_2_left = 12
        self.player_1_kings = self.player_2_kings = 0
        self.create_board()
    
    def draw_squares(self, win):
        """
        The draw squares function draws the squares on the board.
        """
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, self.color, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        """
        The evaluate function evaluates the board to see who is winning and returns the score.
        """
        return self.player_2_left - self.player_1_left + (self.player_2_kings * 0.5 - self.player_1_kings * 0.5)

    def get_all_pieces(self, color):
        """
        The get all pieces function gets all the pieces for a given color and returns the pieces.
        """
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        """
        The move function moves a piece to a given row and column. If the selected row is at the end of the board, the piece becomes a king piece.
        """
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == self.player_2_color:
                self.player_2_kings += 1
            else:
                self.player_1_kings += 1 

    def get_piece(self, row, col): 
        """
        The get piece function gets the piece at a given row and column and returns the piece.
        """
        try:
            return self.board[row][col]
        except:
            return None

    def create_board(self):
        """
        The create board function creates the board with the pieces.
        """
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, self.player_2_color))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, self.player_1_color))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    def draw(self, win): 
        """ 
        The draw function draws the board and the pieces.
        """
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces): 
        """
        The remove function removes a piece from the board in the event that a piece is jumped.
        """
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == self.player_1_color:
                    self.player_1_left -= 1
                else:
                    self.player_2_left -= 1
    
    def winner(self): 
        """
        The winner function checks if a winner has been found and returns the winner. If no winner has been found, None is returned.
        If a user has no pieces left or no moves left, the other user is the winner.
        """
        if self.player_1_left <= 0 or self.no_moves(self.player_1_color):
            return self.player_2_color
        elif self.player_2_left <= 0 or self.no_moves(self.player_2_color):
            return self.player_1_color
        
        return None 
    
    def get_valid_moves(self, piece): 
        """
        The get valid moves function gets all the valid moves for a given piece and returns the moves.
        """
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        if piece.color == self.player_1_color or piece.king:
            moves.update(self.move_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self.move_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == self.player_2_color or piece.king:
            moves.update(self.move_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self.move_right(row +1, min(row+3, ROWS), 1, piece.color, right))

        return moves

    def move_left(self, start, stop, step, color, left, skipped=[]): 
        """
        The move left function moves a piece to the left.
        """
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self.move_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self.move_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
                
            left -= 1
        return moves

    def move_right(self, start, stop, step, color, right, skipped=[]): 
        """
        The move right function moves a piece to the right.
        """
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self.move_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self.move_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves
    
    def no_moves(self, color): 
        """
        The no moves function checks if there are no moves left for a given color and returns True if there are no moves left.
        """
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0 and piece.color == color:
                    valid_moves = self.get_valid_moves(piece)
                    if valid_moves:
                        return False
        return True