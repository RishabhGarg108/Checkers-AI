import pygame
from .constants import Color, ROWS, COLS, SQUARE_SIZE
from .piece import Piece, KingPiece

class Board:
  def __init__(self):
    self.board = []
    self.blackCount = self.whiteCount = 12
    self.blackKings = self.whiteKings = 0
    self.InitializeBoard()
  
  def InitializeBoard(self):
    """Initialise the board and fills the pieces at the starting positions."""
    self.board = [[None for j in range(COLS)] for i in range(ROWS)]
    for row in range(ROWS):
      # (row + 1) % 2 selects the alternate black columns in each row to
      # place the pieces.
      for col in range((row + 1) % 2, COLS, 2):
        if row < 3:
          self.board[row][col] = Piece(row, col, Color.WHITE)
        elif row > 4:
          self.board[row][col] = Piece(row, col, Color.BLACK)

  def GetPiece(self, row, col):
    """Returns the piece present at the (row, col) position"""
    return self.board[row][col]

  def GetAllPieces(self, color):
    """Returns all the pieces of the given color which are currently on the board."""
    pieces = []
    for row in self.board:
      for piece in row:
        if piece and piece.color == color:
          pieces.append(piece)

    return pieces

  def Remove(self, pieces):
    """Remove the pieces from the board.

      @param pieces: List of pieces to remove.
    """
    for piece in pieces:
      self.board[piece.row][piece.col] = None
    if piece:
      if piece.color == Color.WHITE:
        self.whiteCount -= 1
      if piece.color == Color.BLACK:
        self.blackCount -= 1


  def Evaluate(self):
    """Evaluate the score of the current state of board. This is used by
    the AI to evaluate the moves. The White player will try to maximise this
    score and the Black player will minimise this."""
    score = self.whiteCount - self.blackCount + (self.whiteKings - self.blackKings) * 0.5
    return score

  def Winner(self):
    """Checks the winner."""
    if self.blackCount == 0:
      return "White"
    if self.whiteCount == 0:
      return "Black"
    return None

  def Draw(self, win):
    """Draws the board."""
    win.fill(Color.BLACK)

    for row in range(ROWS):
      for col in range(row % 2, COLS, 2):
        pygame.draw.rect(win, 
                         Color.WHITE, 
                         (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
  
    for row in range(ROWS):
      for col in range(COLS):
        piece = self.board[row][col]
        if piece:
          piece.Draw(win)

  def Move(self, selectedPiece, row, col):
    """Moves the selected piece to the input (row, col)."""
    self.board[selectedPiece.row][selectedPiece.col], self.board[row][col] = \
        self.board[row][col], self.board[selectedPiece.row][selectedPiece.col]
    # Since a piece can only move to an empty location in the board, so, only the
    # selected piece needs to be moved.
    selectedPiece.Move(row, col)
    
    # Handles the case if the selected piece becomes a king piece after the move.
    if row == ROWS - 1  or row == 0:
      self.board[selectedPiece.row][selectedPiece.col] = KingPiece(selectedPiece.row, 
                                                                   selectedPiece.col, 
                                                                   selectedPiece.color)
      if selectedPiece.color == Color.BLACK:
        self.blackKings += 1
      else:
        self.whiteKings += 1

  def ValidMoves(self, selectedPiece):
    """Returns a dictionary of valud moves for the selected piece.
    
    @return validMoves: Dictionary of valid moves. Moves are stored as
        { (row, col) : [captured] }
        (row, col) is the position of the valid move.
        [captured] is a list of all the captured pieces in the move.
    """
    row, col = selectedPiece.row, selectedPiece.col
    validMoves = {}

    # Left and right columns.
    left = col - 1
    right = col + 1
    
    if selectedPiece.color == Color.WHITE or selectedPiece.isKing:
      validMoves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, selectedPiece.color, left))
      validMoves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, selectedPiece.color, right))
    
    if selectedPiece.color == Color.BLACK or selectedPiece.isKing:
      validMoves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, selectedPiece.color, left))
      validMoves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, selectedPiece.color, right))

    return validMoves

  def _traverse_left(self, start, stop, step, color, left, skipped=[]):
    """This helper function returns the valid moves in the left diagonal of the piece."""
    validMoves = {}
    last = []

    for r in range(start, stop, step):
      if left < 0:
        break
      
      current = self.board[r][left]
      if current == None:
        if skipped and not last:
          break
        elif skipped:
          validMoves[(r, left)] = last + skipped
        else:
          validMoves[(r, left)] = last

        if last:
          if step == -1:
            row = max(r - 3, 0)
          else:
            row = min(r + 3, ROWS)

          validMoves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
          validMoves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
        break
      # Can not capture our own piece.
      elif current.color == color:
        break
      # Potential opponent piece to capture. Will be checked in the next iteration
      # if it can be captured (when the next position in the diagonal is empty).
      else:
        last = [current]

      left -= 1

    return validMoves

  def _traverse_right(self, start, stop, step, color, right, skipped=[]):
    """This helper function returns the valid moves in the right diagonal of the piece."""
    validMoves = {}
    last = []

    for r in range(start, stop, step):
      if right >= COLS:
        break
      
      current = self.board[r][right]
      if current == None:
        if skipped and not last:
          break
        elif skipped:
          validMoves[(r, right)] = last + skipped
        else:
          validMoves[(r, right)] = last

        if last:
          if step == -1:
            row = max(r - 3, 0)
          else:
            row = min(r + 3, ROWS)

          validMoves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
          validMoves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
        break
      # Can not capture our own piece.
      elif current.color == color:
        break
      # Potential opponent piece to capture. Will be checked in the next iteration
      # if it can be captured (when the next position in the diagonal is empty).
      else:
        last = [current]

      right += 1

    return validMoves
