# Basic Linked List to represent Snake
from node import Node
from random import randint

# Direction constants
UP = (0, -1)     # Direction 0
RIGHT = (1, 0)   # Direction 1
DOWN = (0, 1)    # Direction 2
LEFT = (-1, 0)   # Direction 3
DIR = [UP, RIGHT, DOWN, LEFT]

class Snake:
  def __init__(self, x_max, y_max):
    self.head = Node(x_max//2, y_max//2)
    self.tail = self.head
    self.len = 1

    self.heading = 0

    self.food_x = 0
    self.food_y = 0

    self.x_max = x_max
    self.y_max = y_max

    self.placeFood()
  
  def contains(self, target_x, target_y):
    if self.head == None:
        return False
    else:
        ptr = self.head
        while ptr is not None:
            if ptr.equals(target_x, target_y):
                return True
            ptr = ptr.next
        return False

  # Forward: (default)
  # Left: 1
  # Right: 2
  # Returns the direction tuple associated with a new heading
  def turn(self, turn_dir=0):
    if turn_dir == 1:
      self.heading = ((self.heading + 4) - 1) % 4
    elif turn_dir == 2:
      self.heading = ((self.heading + 4) + 1) % 4

  # Moves snake
  def move(self):
    # Calculate new head position
    new_x, new_y = self.head.move(DIR[self.heading])

    if self.isCollision(new_x, new_y):
      return False

    # Move head to target (push onto linked list)
    temp = self.head
    self.head = Node(new_x, new_y)
    temp.prev = self.head
    self.head.next = temp

    if (new_x == self.food_x and new_y == self.food_y):
      self.len += 1
      self.placeFood()
    else:
      self.tail = self.tail.prev
      self.tail.next = None
    return True

  def isCollision(self, x, y):
    return x < 0 or y < 0 or x >= self.x_max or y >= self.y_max or self.contains(x,y)
  
  def placeFood(self):
    x = randint(0, self.x_max - 1)
    y = randint(0, self.y_max - 1)
    
    if self.contains(x,y):
      self.placeFood()
    else:
      self.food_x = x
      self.food_y = y
