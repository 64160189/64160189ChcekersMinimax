import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, BLUE, WHITE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.blue_left = 8
        self.red_kings = self.white_kings = 0
        self.create_board()
    
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, WHITE, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        return self.blue_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == BLUE:
                self.white_kings += 1
            else:
                self.red_kings += 1 

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 2:
                        self.board[row].append(Piece(row, col, BLUE))
                    elif row > 5:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.blue_left -= 1
    
    def winner(self):
        if self.red_left <= 0:
            return BLUE
        elif self.blue_left <= 0:
            return RED
        
        return None 
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        # For regular red pieces
        if piece.color == RED:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))

        # For regular blue pieces
        if piece.color == BLUE:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        # For kings (allow movement in any direction for multiple squares)
        if piece.king:
            moves.update(self._king_traverse_left(row - 1, -1, -1, piece.color, left))
            moves.update(self._king_traverse_right(row - 1, -1, -1, piece.color, right))
            moves.update(self._king_traverse_left(row + 1, ROWS, 1, piece.color, left))
            moves.update(self._king_traverse_right(row + 1, ROWS, 1, piece.color, right))

    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
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
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
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
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves
    
    def _king_traverse_left(self, start, stop, step, color, left, skipped=[], skipped_piece=None):
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

                # Check for double jumps
                if len(skipped) == 1:
                    next_left = left - 1
                    next_right = left + 1
                    if next_left >= 0:
                        next_up = r - step
                        if next_up >= 0 and self.board[next_up][next_left] == 0:
                            next_moves = self._king_traverse_left(next_up, -1, -1, color, next_left, skipped=skipped)
                            if next_moves is not None:
                                for move, skip in next_moves.items():
                                    moves[move] = skip
                    if next_right < COLS:
                        next_up = r - step
                        if next_up >= 0 and self.board[next_up][next_right] == 0:
                            next_moves = self._king_traverse_right(next_up, -1, -1, color, next_right, skipped=skipped)
                            if next_moves is not None:
                                for move, skip in next_moves.items():
                                    moves[move] = skip

                if last and current == 0 and not skipped_piece:
                    next_moves = self._king_traverse_left(r + step, stop, step, color, left - 1, skipped=last)
                    if next_moves is not None:
                        for move, skip in next_moves.items():
                            moves[move] = skip
                    break  # Break if there are no more valid moves
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _king_traverse_right(self, start, stop, step, color, right, skipped=[], skipped_piece=None):
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
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                # Check for double jumps
                if len(skipped) == 1:
                    next_left = right - 1
                    next_right = right + 1
                    if next_left >= 0:
                        next_up = r - step
                        if next_up >= 0 and self.board[next_up][next_left] == 0:
                            next_moves = self._king_traverse_left(next_up, -1, -1, color, next_left, skipped=skipped)
                            if next_moves is not None:
                                for move, skip in next_moves.items():
                                    moves[move] = skip
                    if next_right < COLS:
                        next_up = r - step
                        if next_up >= 0 and self.board[next_up][next_right] == 0:
                            next_moves = self._king_traverse_right(next_up, -1, -1, color, next_right, skipped=skipped)
                            if next_moves is not None:
                                for move, skip in next_moves.items():
                                    moves[move] = skip

                if last and current == 0 and not skipped_piece:
                    next_moves = self._king_traverse_right(r + step, stop, step, color, right + 1, skipped=last)
                    if next_moves is not None:
                        for move, skip in next_moves.items():
                            moves[move] = skip
                    break  # Break if there are no more valid moves
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves
