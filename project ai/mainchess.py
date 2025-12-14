import random
import copy
import sys

def creat_starting_board():
    board = [
        ['r','n','b','q','k','b','n','r'],
        ['p','p','p','p','p','p','p','p'],


        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],
        ['.','.','.','.','.','.','.','.'],


        ['P','P','P','P','P','P','P','P'],
        ['R','N','B','Q','K','B','N','R'],
    ]
    return board

def print_board(board):
    print() 
    print("    a   b   c   d   e   f   g   h")  
    print("  +---+---+---+---+---+---+---+---+")  
    for row_index in range(8):
        row_number = 8 - row_index
        row_display = str(row_number) + " |"
        for column_index in range(8):
             piece = board[row_index][column_index]
             row_display = row_display + " " + piece + " |"
        print(row_display)
        print("  +---+---+---+---+---+---+---+---+")  # Row border
    print("    a   b   c   d   e   f   g   h")  # Column labels again
    print() 

def new_func(row_display, piece):
    row_display = row_display + " " + piece + " |"
    return row_display # Empty line for spacing

def convert_position_to_indices(position):
    if len(position) != 2:
        return None
    column_letter = position[0]  # First character (like 'e')
    row_character = position[1]  # Second character (like '4')
    if column_letter not in 'abcdefgh':
        return None
    if row_character not in '12345678':
        return None
    column_index = ord(column_letter) - ord('a')
    row_number = int(row_character)
    row_index = 8 - row_number
    return (row_index, column_index)

def indices_to_position(row, col):
    # Useful for printing moves chosen by AI
    col_letter = chr(ord('a') + col)
    row_number = 8 - row
    return f"{col_letter}{row_number}"

def is_white_piece(piece):
    return piece in 'PRNBQK'

def is_black_piece(piece):
    return piece in 'prnbqk'

def is_empty_square(piece):
    return piece == '.'

def is_own_piece(piece, is_white_turn):
    if is_white_turn:
        return is_white_piece(piece)
    else:
        return is_black_piece(piece)

def is_enemy_piece(piece, is_white_turn):
    if is_white_turn:
        return is_black_piece(piece)
    else:
        return is_white_piece(piece)

def is_valid_pawn_move(board, from_row, from_col, to_row, to_col, is_white_turn):
    row_difference = to_row - from_row
    col_difference = abs(to_col - from_col)  # abs() gives absolute value
    destination = board[to_row][to_col]
    if is_white_turn:
        if row_difference == -1 and col_difference == 0:
            return is_empty_square(destination)
        if row_difference == -2 and col_difference == 0 and from_row == 6:
            middle_square = board[from_row - 1][from_col]
            return is_empty_square(middle_square) and is_empty_square(destination)
        if row_difference == -1 and col_difference == 1:
            return is_enemy_piece(destination, is_white_turn)
    else:
        if row_difference == 1 and col_difference == 0:
            return is_empty_square(destination)
        if row_difference == 2 and col_difference == 0 and from_row == 1:
            middle_square = board[from_row + 1][from_col]
            return is_empty_square(middle_square) and is_empty_square(destination)
        if row_difference == 1 and col_difference == 1:
            return is_enemy_piece(destination, is_white_turn)
    return False

def is_valid_rook_move(board, from_row, from_col, to_row, to_col, is_white_turn):
    row_diff = to_row - from_row
    col_diff = to_col - from_col
    if row_diff != 0 and col_diff != 0:
        return False  # Moving diagonally is not allowed
    if row_diff == 0 and col_diff == 0:
        return False
    if row_diff == 0:
        step = 1 if col_diff > 0 else -1
        current_col = from_col + step
        while current_col != to_col:
            if not is_empty_square(board[from_row][current_col]):
                return False  # There's a piece in the way
            current_col = current_col + step
    else:
        step = 1 if row_diff > 0 else -1
        current_row = from_row + step
        while current_row != to_row:
            if not is_empty_square(board[current_row][from_col]):
                return False  # There's a piece in the way
            current_row = current_row + step
    destination = board[to_row][to_col]
    return is_empty_square(destination) or is_enemy_piece(destination, is_white_turn)

def is_valid_knight_move(board, from_row, from_col, to_row, to_col, is_white_turn):
    row_diff = abs(to_row - from_row)
    col_diff = abs(to_col - from_col)
    is_L_shape = (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
    if not is_L_shape:
        return False
    destination = board[to_row][to_col]
    return is_empty_square(destination) or is_enemy_piece(destination, is_white_turn)

def is_valid_bishop_move(board, from_row, from_col, to_row, to_col, is_white_turn):
    row_diff = abs(to_row - from_row)
    col_diff = abs(to_col - from_col)
    if row_diff != col_diff or row_diff == 0:
        return False
    row_step = 1 if to_row > from_row else -1
    col_step = 1 if to_col > from_col else -1
    current_row = from_row + row_step
    current_col = from_col + col_step
    while current_row != to_row:
        if not is_empty_square(board[current_row][current_col]):
            return False  # There's a piece in the way
        current_row = current_row + row_step
        current_col = current_col + col_step
    destination = board[to_row][to_col]
    return is_empty_square(destination) or is_enemy_piece(destination, is_white_turn)

def is_valid_queen_move(board, from_row, from_col, to_row, to_col, is_white_turn):
    return (is_valid_rook_move(board, from_row, from_col, to_row, to_col, is_white_turn) or 
            is_valid_bishop_move(board, from_row, from_col, to_row, to_col, is_white_turn))

def is_valid_king_move(board, from_row, from_col, to_row, to_col, is_white_turn):
    row_diff = abs(to_row - from_row)
    col_diff = abs(to_col - from_col)
    if row_diff > 1 or col_diff > 1:
        return False
    if row_diff == 0 and col_diff == 0:
        return False
    destination = board[to_row][to_col]
    return is_empty_square(destination) or is_enemy_piece(destination, is_white_turn)

def is_valid_move(board, from_row, from_col, to_row, to_col, is_white_turn):
    if not (0 <= from_row <= 7 and 0 <= from_col <= 7):
        return False
    if not (0 <= to_row <= 7 and 0 <= to_col <= 7):
        return False
    piece = board[from_row][from_col]
    if not is_own_piece(piece, is_white_turn):
        return False
    piece_type = piece.lower()
    if piece_type == 'p':
        return is_valid_pawn_move(board, from_row, from_col, to_row, to_col, is_white_turn)
    elif piece_type == 'r':
        return is_valid_rook_move(board, from_row, from_col, to_row, to_col, is_white_turn)
    elif piece_type == 'n':
        return is_valid_knight_move(board, from_row, from_col, to_row, to_col, is_white_turn)
    elif piece_type == 'b':
        return is_valid_bishop_move(board, from_row, from_col, to_row, to_col, is_white_turn)
    elif piece_type == 'q':
        return is_valid_queen_move(board, from_row, from_col, to_row, to_col, is_white_turn)
    elif piece_type == 'k':
        return is_valid_king_move(board, from_row, from_col, to_row, to_col, is_white_turn)
    return False

def make_move(board, from_row, from_col, to_row, to_col):
    """
    Executes move and returns a tuple (captured_piece, was_promotion, original_piece).
    We need original_piece to allow undo (especially for pawn promotion).
    """
    original_piece = board[from_row][from_col]
    captured_piece = board[to_row][to_col]
    piece_to_place = original_piece

    # Handle promotion if any
    was_promotion = False
    if original_piece == 'P' and to_row == 0:
        piece_to_place = 'Q'
        was_promotion = True
    elif original_piece == 'p' and to_row == 7:
        piece_to_place = 'q'
        was_promotion = True

    board[to_row][to_col] = piece_to_place
    board[from_row][from_col] = '.'

    return (captured_piece, was_promotion, original_piece)

def undo_move(board, from_row, from_col, to_row, to_col, captured_piece, was_promotion, original_piece):
    """
    Reverts a move using the data returned by make_move.
    """
    # Restore from square
    board[from_row][from_col] = original_piece
    # Restore destination
    board[to_row][to_col] = captured_piece

def get_all_legal_moves(board, is_white_turn):
    """
    Returns list of moves as tuples: (from_row, from_col, to_row, to_col)
    Uses current is_valid_move logic (no check detection).
    """
    moves = []
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece == '.':
                continue
            if not is_own_piece(piece, is_white_turn):
                continue
            for tr in range(8):
                for tc in range(8):
                    if is_valid_move(board, r, c, tr, tc, is_white_turn):
                        moves.append((r, c, tr, tc))
    return moves

# Simple evaluation function (material)
PIECE_VALUES = {
    'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 1000,
    'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -1000,
    '.': 0
}

def evaluate_board(board):
    total = 0
    for row in board:
        for piece in row:
            if piece in PIECE_VALUES:
                total += PIECE_VALUES[piece]
    return total

def minimax(board, depth, is_white_turn, alpha, beta):
    """
    Returns (best_score, best_move)
    best_move is tuple (from_row, from_col, to_row, to_col) or None
    """
    if depth == 0:
        return evaluate_board(board), None

    moves = get_all_legal_moves(board, is_white_turn)
    if not moves:
        # No legal moves according to current move generation
        return evaluate_board(board), None

    best_move = None
    if is_white_turn:
        max_eval = -10**9
        for move in moves:
            fr, fc, tr, tc = move
            captured, was_prom, orig = make_move(board, fr, fc, tr, tc)
            eval_score, _ = minimax(board, depth - 1, False, alpha, beta)
            undo_move(board, fr, fc, tr, tc, captured, was_prom, orig)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = 10**9
        for move in moves:
            fr, fc, tr, tc = move
            captured, was_prom, orig = make_move(board, fr, fc, tr, tc)
            eval_score, _ = minimax(board, depth - 1, True, alpha, beta)
            undo_move(board, fr, fc, tr, tc, captured, was_prom, orig)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

def pick_ai_move(board, is_white_turn, level='medium'):
    """
    level: 'easy' (random), 'medium' (minimax depth 2), 'hard' (minimax depth 3)
    """
    moves = get_all_legal_moves(board, is_white_turn)
    if not moves:
        return None

    if level == 'easy':
        return random.choice(moves)
    elif level == 'medium':
        _, move = minimax(board, 2, is_white_turn, -10**9, 10**9)
        if move is None:
            return random.choice(moves)
        return move
    elif level == 'hard':
        _, move = minimax(board, 3, is_white_turn, -10**9, 10**9)
        if move is None:
            return random.choice(moves)
        return move
    else:
        # default to medium
        _, move = minimax(board, 2, is_white_turn, -10**9, 10**9)
        return move if move is not None else random.choice(moves)

def get_player_move():
    print("Enter your move (example: e2 e4)")
    print("Or type 'quit' to exit the game")
    user_input = input("> ").strip().lower()
    if user_input == 'quit':
        return ('quit', 'quit')
    parts = user_input.split()
    if len(parts) != 2:
        print("Invalid format! Please use format: e2 e4")
        return None
    from_position = parts[0]
    to_position = parts[1]
    return (from_position, to_position)

def play_game():
    board = creat_starting_board()
    is_white_turn = True
    move_number = 1

    # Choose opponent mode
    print("=" * 50)
    print("      WELCOME TO SIMPLE CHESS WITH AI!")
    print("=" * 50)
    print("1) Human vs Human")
    print("2) Human vs AI")
    mode = input("Choose mode (1 or 2): ").strip()
    ai_level = 'medium'
    ai_plays_white = False
    if mode == '2':
        print("AI levels: easy, medium, hard")
        ai_level = input("Choose AI level (easy/medium/hard): ").strip().lower()
        side = input("Do you want to play White or Black? (w/b): ").strip().lower()
        if side == 'w':
            ai_plays_white = False
        else:
            ai_plays_white = True

    print("White pieces: P R N B Q K (uppercase)")
    print("Black pieces: p r n b q k (lowercase)")
    print("Empty squares: .")
    print("Enter moves like: e2 e4")
    print("Type 'quit' to exit the game")
    print("=" * 50)

    while True:
        print_board(board)
        if is_white_turn:
            print(f"Move {move_number}: WHITE's turn")
        else:
            print(f"Move {move_number}: BLACK's turn")

        # Decide if AI moves this turn
        this_turn_is_ai = (mode == '2') and (is_white_turn == ai_plays_white)

        if this_turn_is_ai:
            print("AI is thinking...")
            ai_move = pick_ai_move(board, is_white_turn, level=ai_level)
            if ai_move is None:
                print("AI has no legal moves. Game over or stalemate (not fully detected).")
                break
            fr, fc, tr, tc = ai_move
            captured, was_prom, orig = make_move(board, fr, fc, tr, tc)
            print(f"AI moved: {indices_to_position(fr, fc)} to {indices_to_position(tr, tc)}")
        else:
            move = get_player_move()
            if move is None:
                continue
            if move[0] == 'quit':
                print("\nThank you for playing! Goodbye!")
                break
            from_position = move[0]
            to_position = move[1]
            from_indices = convert_position_to_indices(from_position)
            to_indices = convert_position_to_indices(to_position)
            if from_indices is None:
                print(f"Invalid starting position: {from_position}")
                continue
            if to_indices is None:
                print(f"Invalid destination: {to_position}")
                continue
            from_row, from_col = from_indices
            to_row, to_col = to_indices
            if not is_valid_move(board, from_row, from_col, to_row, to_col, is_white_turn):
                print("Invalid move! Please try again.")
                continue
            make_move(board, from_row, from_col, to_row, to_col)
            if is_white_turn:
                print(f"White moved: {from_position} to {to_position}")
            else:
                print(f"Black moved: {from_position} to {to_position}")

        is_white_turn = not is_white_turn
        if is_white_turn:
            move_number = move_number + 1

if __name__ == "__main__":
    play_game()