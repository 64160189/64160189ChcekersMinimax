from copy import deepcopy       #deepcopy คือ copy ค่าเริ่มต้นตั้งแต่แรก ก็อปมาแล้วก็ไม่เกี่ยวข้องกันอีกแล้ว
from checkers.constants import RED, BLUE
import pygame

def minimax(position, depth, max_player, game):
    if depth == 0 or position.winner() != None:     #ถ้ายังไม่มีผู้ชนะ return position
        return position.evaluate(), position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None 
        for move in get_all_moves(position, BLUE, game):        #get all moves and calculate the best move
            evaluation = minimax(move, depth-1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move                
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth-1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move


def simulate_move(piece, move, board, game, skip):      
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board        #move and return board after move


def get_all_moves(board, color, game):       #รับ move ที่เป็นไปได้ทั้งหมดจาก position ตอนนี้
    moves = []

    for piece in board.get_all_pieces(color):       #loop all pieces in the board
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            #draw_moves(game, board, piece)     #call draw_moves to draw animation while AI find all moves
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)     
            moves.append(new_board)
    
    return moves


def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)  
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    #pygame.time.delay(10)     #เพิ่มการเวลาทำงาน ของ animation นี้
