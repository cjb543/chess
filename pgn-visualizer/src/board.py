from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPixmap
from PyQt6.QtCore import Qt
import re
import os
import sys

class ChessBoard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.square_size = 40
        self.board_size = self.square_size * 8
        self.setMinimumSize(200, 200)
        self.pieces = {}
        self.piece_images = {}
        self.setupStartingPosition()
        self.loadPieceImages()
        self.current_position = {}
        self.positions_history = []
        self.current_move_index = -1
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        start_x = (self.width() - self.board_size) // 2
        start_y = (self.height() - self.board_size) // 2
        for row in range(8):
            for col in range(8):
                x = start_x + col * self.square_size
                y = start_y + row * self.square_size
                if (row + col) % 2 == 0:
                    color = QColor(240, 217, 181)
                else:
                    color = QColor(181, 136, 99)
                painter.fillRect(x, y, self.square_size, self.square_size, color)

        display_position = self.getCurrentPosition()

        for (row, col), piece_type in display_position.items():
            if piece_type in self.piece_images:
                pixmap = self.piece_images[piece_type]
                if not pixmap.isNull():
                    x = start_x + col * self.square_size
                    y = start_y + row * self.square_size
                    offset_x = (self.square_size - pixmap.width()) // 2
                    offset_y = (self.square_size - pixmap.height()) // 2
                    painter.drawPixmap(x + offset_x, y + offset_y, pixmap)
    
    def setupStartingPosition(self):
        self.pieces = {}
        for col in range(8):
            self.pieces[(1, col)] = "bP"
            self.pieces[(6, col)] = "wP"
        back_row_pieces = ["R", "N", "B", "Q", "K", "B", "N", "R"]
        for col in range(8):
            self.pieces[(0, col)] = "b" + back_row_pieces[col]
            self.pieces[(7, col)] = "w" + back_row_pieces[col]
        self.positions_history = []
        self.current_move_index = -1
    
    def loadPieceImages(self):
        import os
        import sys
        
        def get_base_path():
            """Get base path for resources"""
            if getattr(sys, 'frozen', False):
                # If the application is run as a bundle
                return sys._MEIPASS
            else:
                # If the application is run in development
                return os.path.dirname(os.path.abspath(__file__))
        
        piece_types = [
            "wP", "wR", "wN", "wB", "wQ", "wK",
            "bP", "bR", "bN", "bB", "bQ", "bK"
        ]
        
        base_path = get_base_path()
        
        for piece_type in piece_types:
            # Try multiple possible locations
            possible_paths = [
                os.path.join(base_path, f"{piece_type}.png"),  # Direct in base path
                os.path.join(base_path, "assets", f"{piece_type}.png"),  # In assets subfolder
                f"assets/{piece_type}.png",  # Relative path (original)
                f"{piece_type}.png"  # Just filename
            ]
            
            pixmap = None
            loaded_path = None
            
            # Try each path until one works
            for path in possible_paths:
                print(f"Trying to load piece from: {path}")
                temp_pixmap = QPixmap(path)
                if not temp_pixmap.isNull():
                    pixmap = temp_pixmap
                    loaded_path = path
                    break
                
            if pixmap:
                print(f"Successfully loaded {piece_type} from {loaded_path}")
                pixmap = pixmap.scaled(
                    self.square_size,
                    self.square_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            else:
                print(f"FAILED to load {piece_type} from any location")
                
            self.piece_images[piece_type] = pixmap

    def getCurrentPosition(self):
        if self.current_move_index == -1:
            return self.pieces
        elif 0 <= self.current_move_index < len(self.positions_history):
            return self.positions_history[self.current_move_index]
        return self.pieces
    
    def parsePGN(self, pgn_content):
        self.setupStartingPosition()
        moves_text = self.extractMovesFromPGN(pgn_content)
        moves = self.extractMovesList(moves_text)
        self.generatePositionsFromMoves(moves)
        self.update()
    
    def extractMovesFromPGN(self, pgn_content):
        if '\n\n' in pgn_content:
            return pgn_content.split('\n\n', 1)[1]
        return pgn_content
    
    def extractMovesList(self, moves_text):
        moves_text = re.sub(r'\{[^}]*\}', '', moves_text)
        moves_text = re.sub(r'\([^)]*\)', '', moves_text)
        moves_text = re.sub(r'1-0|0-1|1/2-1/2|\*', '', moves_text)
        move_pattern = r'(?:\d+\.+\s*)?([KQRBNP]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?|O-O(?:-O)?)'
        moves = re.findall(move_pattern, moves_text)
        return [move for move in moves if move.strip()]
    
    def applyMoveToPosition(self, move, position, player):
        new_position = position.copy()
        if move == "O-O":
            if player == 'w':
                if (7, 4) in new_position and (7, 7) in new_position:
                    new_position[(7, 6)] = new_position.pop((7, 4))
                    new_position[(7, 5)] = new_position.pop((7, 7))
                else:
                    print(f"Warning: Cannot castle, pieces not in expected positions")
            else:
                if (0, 4) in new_position and (0, 7) in new_position:
                    new_position[(0, 6)] = new_position.pop((0, 4))
                    new_position[(0, 5)] = new_position.pop((0, 7))
                else:
                    print(f"Warning: Cannot castle, pieces not in expected positions")
            return new_position
        if move == "O-O-O":
            if player == 'w':
                new_position[(7, 2)] = new_position.pop((7, 4))
                new_position[(7, 3)] = new_position.pop((7, 0))
            else:
                new_position[(0, 2)] = new_position.pop((0, 4))
                new_position[(0, 3)] = new_position.pop((0, 0))
            return new_position
        move_data = self.parseMoveNotation(move, player)
        source_square = self.findSourceSquare(move_data, new_position, player)
        if source_square:
            target_square = (move_data['target_row'], move_data['target_col'])
            if target_square in new_position:
                del new_position[target_square]
            piece = new_position.pop(source_square)
            if move_data['promotion']:
                piece = player + move_data['promotion']
            new_position[target_square] = piece 
        return new_position
    
    def parseMoveNotation(self, move, player):
        result = {
            'piece': 'P',
            'source_file': None,
            'source_rank': None,
            'target_col': None,
            'target_row': None,
            'is_capture': 'x' in move,
            'promotion': None
        }
        move = move.replace('+', '').replace('#', '')
        if '=' in move:
            move_part, promotion = move.split('=')
            result['promotion'] = promotion
            move = move_part
        if move[0] in "KQRBNP":
            result['piece'] = move[0]
            move = move[1:]
        target_file = move[-2]
        target_rank = move[-1]
        result['target_col'] = ord(target_file) - ord('a')
        result['target_row'] = 8 - int(target_rank)
        move = move[:-2]
        if 'x' in move:
            move = move.replace('x', '')
        if len(move) > 0 and 'a' <= move[0] <= 'h':
            result['source_file'] = ord(move[0]) - ord('a')   
        if len(move) > 0 and '1' <= move[-1] <= '8':
            result['source_rank'] = 8 - int(move[-1])
        return result
    
    def findSourceSquare(self, move_data, position, player):
        piece_code = player + move_data['piece']
        target_row = move_data['target_row']
        target_col = move_data['target_col']
        candidates = []
        if move_data['piece'] == 'P' and move_data['source_file'] is None and not move_data['is_capture']:
            if player == 'w':
                if (target_row + 1, target_col) in position and position[(target_row + 1, target_col)] == 'wP':
                    return (target_row + 1, target_col)
                elif target_row == 4 and (6, target_col) in position and position[(6, target_col)] == 'wP':
                    return (6, target_col)
            else:
                if (target_row - 1, target_col) in position and position[(target_row - 1, target_col)] == 'bP':
                    return (target_row - 1, target_col)
                elif target_row == 3 and (1, target_col) in position and position[(1, target_col)] == 'bP':
                    return (1, target_col)
        elif move_data['piece'] == 'P' and move_data['is_capture'] and move_data['source_file'] is not None:
            source_col = move_data['source_file']
            if player == 'w':
                if (target_row + 1, source_col) in position and position[(target_row + 1, source_col)] == 'wP':
                    return (target_row + 1, source_col)
            else:
                if (target_row - 1, source_col) in position and position[(target_row - 1, source_col)] == 'bP':
                    return (target_row - 1, source_col)
        for (row, col), piece in position.items():
            if piece == piece_code:
                if move_data['source_file'] is not None and col != move_data['source_file']:
                    continue
                if move_data['source_rank'] is not None and row != move_data['source_rank']:
                    continue
                if piece_code[1] == 'P':
                    if not move_data['is_capture']:
                        if player == 'w' and not (row > target_row and col == target_col):
                            continue
                        if player == 'b' and not (row < target_row and col == target_col):
                            continue
                    else:
                        if player == 'w' and not (row > target_row and abs(col - target_col) == 1):
                            continue
                        if player == 'b' and not (row < target_row and abs(col - target_col) == 1):
                            continue
                elif piece_code[1] == 'N':
                    if not ((abs(row - target_row) == 2 and abs(col - target_col) == 1) or 
                            (abs(row - target_row) == 1 and abs(col - target_col) == 2)):
                        continue
                elif piece_code[1] == 'B':
                    if abs(row - target_row) != abs(col - target_col):
                        continue
                    if not self.isDiagonalPathClear(position, row, col, target_row, target_col):
                        continue
                elif piece_code[1] == 'R':
                    if row != target_row and col != target_col:
                        continue
                    if not self.isStraightPathClear(position, row, col, target_row, target_col):
                        continue
                elif piece_code[1] == 'Q':
                    if row != target_row and col != target_col and abs(row - target_row) != abs(col - target_col):
                        continue
                    if row == target_row or col == target_col:
                        if not self.isStraightPathClear(position, row, col, target_row, target_col):
                            continue
                    else:
                        if not self.isDiagonalPathClear(position, row, col, target_row, target_col):
                            continue
                elif piece_code[1] == 'K':
                    if abs(row - target_row) > 1 or abs(col - target_col) > 1:
                        continue
                candidates.append((row, col))
        if len(candidates) == 1:
            return candidates[0]
        elif len(candidates) > 1:
            print(f"Multiple candidates for move: {candidates}, choosing first")
            return candidates[0]
        print(f"No valid source found for {player}{move_data['piece']} to ({target_row},{target_col})")
        return None

    def isDiagonalPathClear(self, position, start_row, start_col, end_row, end_col):
        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1
        row, col = start_row + row_step, start_col + col_step
        while (row, col) != (end_row, end_col):
            if (row, col) in position:
                return False
            row += row_step
            col += col_step
        return True

    def isStraightPathClear(self, position, start_row, start_col, end_row, end_col):
        if start_row == end_row:
            col_step = 1 if end_col > start_col else -1
            for col in range(start_col + col_step, end_col, col_step):
                if (start_row, col) in position:
                    return False
        else:
            row_step = 1 if end_row > start_row else -1
            for row in range(start_row + row_step, end_row, row_step):
                if (row, start_col) in position:
                    return False
        return True

    def generatePositionsFromMoves(self, moves):
        current_position = self.pieces.copy()
        current_player = 'w'
        self.positions_history = []
        for i, move in enumerate(moves):
            print(f"Processing move {i+1}: {move} by {current_player}")
            try:
                current_position = self.applyMoveToPosition(move, current_position, current_player)
                self.positions_history.append(current_position.copy())
                current_player = 'b' if current_player == 'w' else 'w'
            except Exception as e:
                print(f"Error at move {i+1} ({move}): {e}")
                break
    
    def nextMove(self):
        if self.current_move_index < len(self.positions_history) - 1:
            self.current_move_index += 1
            self.update()
            return True
        return False
    
    def previousMove(self):
        if self.current_move_index >= 0:
            self.current_move_index -= 1
            self.update()
            return True
        return False
    
    def resetToStart(self):
        self.current_move_index = -1
        self.update()