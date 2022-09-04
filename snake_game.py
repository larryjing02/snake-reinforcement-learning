from snake import Snake
from time import sleep
from math import sqrt
import pygame

pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

GAME_CYCLE_DELAY = False
GAME_OVER_DELAY = False
GAME_CYCLE_TIME = 0.1
GAME_OVER_TIME = 5

# Set up the drawing window
window_blocks_x = 16
window_blocks_y = 16
block_size = 40
block_border = 2

class SnakeGame:
  def __init__(self):
    self.screen = pygame.display.set_mode([window_blocks_x*block_size, window_blocks_y*block_size])
    
    self.resetGame()
  
  def resetGame(self):
    # Snake set as a list of tuples, each representing a point
    self.snake = Snake(window_blocks_x, window_blocks_y)
    self.iterations = 0

  def refreshScreen(self):
    self.screen.fill(BLACK)
    
    # Draw snake body
    cur = self.snake.head
    while cur:
      self.drawPoint(cur.x, cur.y, WHITE)
      cur = cur.next
    
    # Draw food
    self.drawPoint(self.snake.food_x, self.snake.food_y, GREEN)

    # Flip the display
    pygame.display.flip()
    

  def drawPoint(self, x, y, color):
    point = (x*block_size+block_border, y*block_size+block_border)
    rect = pygame.Rect(point, (block_size-2*block_border, block_size-2*block_border))
    pygame.draw.rect(self.screen, color, rect)

  def step(self, turn=0):
    # Did the user click the window close button?
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
      # Take user input
      # if event.type == pygame.KEYDOWN:
      #   if event.key == pygame.K_LEFT:
      #     self.snake.turn(1)
      #   elif event.key == pygame.K_RIGHT:
      #     self.snake.turn(2)
    self.snake.turn(turn)
    
    self.iterations += 1

    # Make move; 0 = died, 1 = survived, 2 = ate food
    result = self.snake.move()
    if self.iterations < 100*self.snake.len and result > 0:
      self.refreshScreen()
      reward = self.distToFood()
      if result == 2:
        reward += 10
      if GAME_CYCLE_DELAY:
        sleep(GAME_CYCLE_TIME)
      return reward, False, self.snake.len
    else:
      print(f"Final Score: {self.snake.len}")
      if GAME_OVER_DELAY:
        sleep(GAME_OVER_TIME)
      return -10, True, self.snake.len

  def distToFood(self):
    delta_x = self.snake.head.x - self.snake.food_x
    delta_y = self.snake.head.y - self.snake.food_y
    return int(window_blocks_x/2-sqrt(delta_x**2 + delta_y**2))
    
# if __name__ == '__main__':
#   game = SnakeGame()
  
#   # game loop
#   while True:
#       reward, result, score = game.step()
#       # print(f"Reward: {reward}")
#       if result:
#         game.resetGame()

      
#   pygame.quit()