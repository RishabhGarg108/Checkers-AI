import pygame
from .constants import *
from .board import Board

class Game:
  def __init__(self, win):
    self._Init()
    self.win = win

  def Reset(self):
    """Resets the game."""
    self._Init()

  def _Init(self):
    """Initialises the members of the class."""
    self.selectedPiece = None
    self.board = Board()
    self.turn = Color.BLACK
    self.validMoves = {}

  def GetBoard(self):
    """Returns the board."""
    return self.board

  def Winner(self):
    """Returns the winner when game is finished."""
    return self.board.Winner()

  def Select(self, row, col):
    """This is for the human player. All the human interactions are in form
    of selecting some piece or location. Based on the possible cases, different
    actions are performed when the player selects something."""
    piece = self.board.GetPiece(row, col)
    
    # If the selected piece is clicked again, it is deselected.
    if self.selectedPiece and self.selectedPiece == piece:
      self.selectedPiece.ToggleSelect()
      self.selectedPiece = None
      # Reset the valid moves because nothing is selected.
      self.validMoves = {}
    else:
      # If nothing is selected, then try to select the clicked piece.
      if not self.selectedPiece:
        # Can not select a piece at an empty location or the opposite player's
        # piece.
        if not piece or piece.color != self.turn:
          return

        # Selecting the clicked piece and calculating its valid moves.
        self.selectedPiece = piece
        self.selectedPiece.ToggleSelect()
        self.validMoves = self.board.ValidMoves(self.selectedPiece)
      # A piece is already selected. Try to move the selected piece to the location
      # which is currently clicked.
      else:
        # Can only move to an empty location and that too when it is one of the
        # valid moves.
        if not piece:
          if (row, col) in self.validMoves:
            self._move(row, col)
            self.selectedPiece.ToggleSelect()
            self.ChangePlayer()           

        # If the same player's piece is selected again, then deselect the previous
        # piece and select this one.
        elif piece.color == self.turn:
          self.selectedPiece.ToggleSelect()
          self.selectedPiece = piece
          self.selectedPiece.ToggleSelect()
          self.validMoves = self.board.ValidMoves(self.selectedPiece)

  def _move(self, row, col):
    """Moves the selected piece to (row, col)."""
    self.board.Move(self.selectedPiece, row, col)

    # Delete the captured pieces from the board.
    captured = self.validMoves[(row, col)]
    if captured:
      self.board.Remove(captured)
    
  def ChangePlayer(self):
    """Changes the turn in game."""
    self.selectedPiece = None
    self.validMoves = {}
    self.turn = Color.BLACK if self.turn == Color.WHITE else Color.WHITE

  def AIMove(self, board):
    """Makes a move for AI. Sets the game's board to the input board which
    is the state of board after the AI's moves"""
    self.board = board
    self.ChangePlayer()

  def DrawValidMoves(self):
    """Draws a small green dot on the valid moves for the selected piece."""
    for (row, col) in self.validMoves:
      radius = 5
      x = col * SQUARE_SIZE + SQUARE_SIZE // 2 - radius
      y = row * SQUARE_SIZE + SQUARE_SIZE // 2 - radius
      pygame.draw.circle(self.win, Color.GREEN, (x, y), radius)
    pygame.display.update()

  def Update(self):
    """Draws everything and updates the pygame diaplay."""
    self.board.Draw(self.win)
    self.DrawValidMoves()
    pygame.display.update()
