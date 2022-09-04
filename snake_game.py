from snake import Snake
from time import sleep
import pygame

pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

GAME_CYCLE_DELAY = True
GAME_CYCLE_TIME = 0.1
GAME_OVER_TIME = 5


# Set up the drawing window
# window_blocks_x = 8
# window_blocks_y = 8
# block_size = 40
# block_border = 2
window_blocks_x = 80
window_blocks_y = 80
block_size = 8
block_border = 1
screen = pygame.display.set_mode([window_blocks_x*block_size, window_blocks_y*block_size])



# Snake set as a list of tuples, each representing a point
snake = Snake(window_blocks_x, window_blocks_y)
heading = 0


def refreshScreen():
  screen.fill(BLACK)
  
  cur = snake.head
  while cur:
    drawPoint(cur.x, cur.y, WHITE)
    cur = cur.next
  
  drawPoint(snake.food_x, snake.food_y, GREEN)


  # Flip the display
  pygame.display.flip()

def drawPoint(x, y, color):
  point = (x*block_size+block_border, y*block_size+block_border)
  rect = pygame.Rect(point, (block_size-2*block_border, block_size-2*block_border))
  pygame.draw.rect(screen, color, rect)

# Run until the user asks to quit
running = True
while running:

  # Did the user click the window close button?
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      break
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        snake.turn(1)
      elif event.key == pygame.K_RIGHT:
        snake.turn(2)
    
  if snake.move():
    refreshScreen()
    # print("------------------------")
    # print(snake.head)
    # print("------------------------")
  else:
    print(f"Final Score: {snake.len}")
    sleep(GAME_OVER_TIME)
    running = False

  if GAME_CYCLE_DELAY:
    sleep(GAME_CYCLE_TIME)





pygame.quit()