import pygame
from checkers.constants import *

class Piece:
  PADDING = 17
  BORDER = 3
  BORDER_COLOR = Color.GREY

  def __init__(self, row, col, color, isKing = False):
    self.row = row
    self.col = col
    self.color = color
    self.isSelected = False
    self.isKing = isKing
    self.x, self.y = self._CalculateCenterPos()
  
  def _CalculateCenterPos(self):
    """Calculate the centre cooredinates of the square where the piece
    is present."""
    x = SQUARE_SIZE * self.col + SQUARE_SIZE//2
    y = SQUARE_SIZE * self.row + SQUARE_SIZE//2

    return x, y

  def ToggleSelect(self):
    """Toggles whether the piece is selected or not."""
    self.isSelected = not self.isSelected
  
  def Move(self, row, col):
    """Moves the piece to the specified row and col."""
    self.row = row
    self.col = col
    # Recalculating center 
    self.x, self.y = self._CalculateCenterPos()

  def Draw(self, win):
    """Draw the piece on board."""
    radius = SQUARE_SIZE//2 - self.PADDING
    # Draws the border around piece.
    pygame.draw.circle(win, self.BORDER_COLOR, (self.x, self.y),
        radius + self.BORDER)
    # Draws the piece.
    pygame.draw.circle(win, self.color, (self.x, self.y), radius)

    # If the piece is selected, a grey boundary appears around it.
    if self.isSelected:
      pygame.draw.rect(win,
          Color.GREY,
          (self.col * SQUARE_SIZE, self.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
          5)

  def __repr__(self):
    return f"Row: {self.row}, Col: {self.col}, Color: {self.color}"


class KingPiece(Piece):
  def __init__(self, row, col, color):
    super().__init__(row, col, color, isKing = True)

  def Draw(self, win):
    radius = SQUARE_SIZE//2 - self.PADDING
    pygame.draw.circle(win, self.BORDER_COLOR, (self.x, self.y),
        radius + self.BORDER)
    ## TODO: Replace Color.RED with self.color once pygame image load is fixed.
    pygame.draw.circle(win, Color.RED, (self.x, self.y), radius)
    # win.blit(CROWN, 
    #     (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    if self.isSelected:
      pygame.draw.rect(win,
          Color.GREY,
          (self.col * SQUARE_SIZE, self.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
          5)
