from copy import deepcopy
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def Minimax(currentBoard, depth, maxPlayer, game):
  """The minimax algorithm. Returns the best score and the board
  after making the best possible move."""
  # We are a leaf node. Evaluating the board.
  if depth == 0 or currentBoard.Winner() != None:
    return currentBoard.Evaluate(), currentBoard

  if maxPlayer:
    maxScore = float("-inf")
    bestMove = None

    for boardPosition in GetAllMoves(currentBoard, WHITE, game):
      score, _ = Minimax(boardPosition, depth - 1, False, game)
      maxScore = max(score, maxScore)

      if maxScore == score:
        bestMove = boardPosition

    return maxScore, bestMove

  else:
    minScore = float("inf")
    bestMove = None

    for boardPosition in GetAllMoves(currentBoard, BLACK , game):
      score, _ = Minimax(boardPosition, depth - 1, True, game)
      minScore = min(score, minScore)

      if minScore == score:
        bestMove = boardPosition

    return minScore, bestMove

def SimulateMove(piece, move, board, game, captured):
  """Simulates the move of AI."""
  board.Move(piece, *move)

  if captured:
    board.Remove(captured)

  return board

def GetAllMoves(currentBoard, color, game):
  """Takes the current board and returns a list of new boards for all the valid
  moves of all the pieces of the given color."""
  moves = []
  
  for piece in currentBoard.GetAllPieces(color):
    validMoves = currentBoard.ValidMoves(piece)

    for move, captured in validMoves.items():
      # Deep copying the board to avoid changes to the game state.
      tempBoard = deepcopy(currentBoard)
      tempPiece = tempBoard.GetPiece(piece.row, piece.col)

      newBoard = SimulateMove(tempPiece, move, tempBoard, game, captured)
      moves.append(newBoard)

  return moves
