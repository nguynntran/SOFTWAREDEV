import pygame
from .board import Board
from .constants import Cons

class Game:
    def __init__(self):
        self.board = Board()
        self.current_player = Cons.WOLF  # Wolves start first
        self.game_over = False
        self.winner = None
        self.move_count = 0
        self.max_moves = 100  # Prevent infinite games
    
    def handle_click(self, pos):
        """Handle mouse clicks on the board"""
        if self.game_over:
            return
        
        col = pos[0] // Cons.SQUARE_SIZE
        row = pos[1] // Cons.SQUARE_SIZE
        
        # Check if click is within board bounds
        if not (0 <= row < Cons.ROWS and 0 <= col < Cons.COLS):
            return
        
        # Only allow moves on dark squares (white squares is invalid)
        if (row + col) % 2 == 0:
            return
        
        piece = self.board.board[row][col]
        
        # If no piece is selected
        if self.board.selected_piece is None:
            if piece and piece.type == self.current_player:
                self.board.selected_piece = (row, col)
                self.board.highlight = piece.get_legal_moves(self.board.board)
        else:
            # If clicking on highlighted square, move piece
            if (row, col) in self.board.highlight:
                self.make_move(self.board.selected_piece, (row, col))
                self.board.selected_piece = None
                self.board.highlight = []
                self.switch_player()
                self.check_win_condition()
            # If clicking on own piece, select it
            elif piece and piece.type == self.current_player:
                self.board.selected_piece = (row, col)
                self.board.highlight = piece.get_legal_moves(self.board.board)
            # If clicking elsewhere, deselect
            else:
                self.board.selected_piece = None
                self.board.highlight = []
    
    def make_move(self, from_pos, to_pos):
        """Move a piece from one position to another"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board.board[from_row][from_col]
        if piece:
            piece.move(to_row, to_col)
            self.board.board[to_row][to_col] = piece
            self.board.board[from_row][from_col] = None
            self.move_count += 1
    
    def switch_player(self):
        """Switch between wolf and sheep turns"""
        self.current_player = Cons.SHEEP if self.current_player == Cons.WOLF else Cons.WOLF
    
    def check_win_condition(self):
        """Check if the game has ended and determine winner"""
        # Find all wolves and sheep
        wolves = []
        sheep = []
        
        for row in range(Cons.ROWS):
            for col in range(Cons.COLS):
                piece = self.board.board[row][col]
                if piece:
                    if piece.type == Cons.WOLF:
                        wolves.append(piece)
                    elif piece.type == Cons.SHEEP:
                        sheep.append(piece)
        
        # Check if sheep reached the top row (wolves' starting row)
        for sheep_piece in sheep:
            if sheep_piece.row == 0:
                self.game_over = True
                self.winner = Cons.SHEEP
                return
        
        # Check if wolves are blocked (no legal moves)
        wolf_can_move = False
        for wolf in wolves:
            if wolf.get_legal_moves(self.board.board):
                wolf_can_move = True
                break
        
        if not wolf_can_move and self.current_player == Cons.WOLF:
            self.game_over = True
            self.winner = Cons.SHEEP
            return
        
        # Check if sheep is surrounded
        sheep_can_move = False
        for sheep_piece in sheep:
            if sheep_piece.get_legal_moves(self.board.board):
                sheep_can_move = True
                break
        
        if not sheep_can_move and self.current_player == Cons.SHEEP:
            self.game_over = True
            self.winner = Cons.WOLF
            return
        
        # Check for draw (too many moves)
        if self.move_count >= self.max_moves:
            self.game_over = True
            self.winner = None  # Draw
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.board = Board()
        self.current_player = Cons.WOLF
        self.game_over = False
        self.winner = None
        self.move_count = 0
    
    def draw(self, screen):
        """Draw the game state"""
        self.board.draw_board(screen)
        
        # Draw game status
        font = pygame.font.Font(None, 36)
        
        if self.game_over:
            if self.winner == Cons.WOLF:
                text = "Wolves Win!"
                color = Cons.GREEN
            elif self.winner == Cons.SHEEP:
                text = "Sheep Wins!"
                color = Cons.YELLOW
            else:
                text = "Draw!"
                color = Cons.WHITE
        else:
            if self.current_player == Cons.WOLF:
                text = "Wolves' Turn"
                color = Cons.GREEN
            else:
                text = "Sheep's Turn"
                color = Cons.YELLOW
        
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (10, 10))
        
        # Draw move counter
        move_text = font.render(f"Moves: {self.move_count}", True, Cons.WHITE)
        screen.blit(move_text, (10, 50))
    
    def get_current_player(self):
        return self.current_player
    
    def is_game_over(self):
        return self.game_over
    
    def get_winner(self):
        return self.winner