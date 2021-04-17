import pygame
from checkers.constants import SQUARE_SIZE, Color, WIDTH, HEIGHT
from checkers.game import Game
from ai.minimax import Minimax
from time import sleep

FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers-AI")

def GetRowColFromMouse(pos):
  """It takes the current position of mouse and returns the
  row and column of the square on the board."""
  x,y = pos
  row = y // SQUARE_SIZE
  col = x // SQUARE_SIZE
  return row, col

def main():
  run = True
  clock = pygame.time.Clock()

  game = Game(WIN)

  while run:
    clock.tick(FPS)

    # AI move.
    if game.turn == Color.WHITE:
      score, newBoard = Minimax(game.GetBoard(), 3, Color.WHITE, game)
      game.AIMove(newBoard)

    if game.Winner() != None:
      print(game.Winner())
      game.Reset()
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
      
      if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        row, col = GetRowColFromMouse(pos)
        game.Select(row, col)

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          game.Reset()

    game.Update()
  pygame.quit()


if __name__ == "__main__":
  main()