# Represents one snake segment
class Node:
  def __init__(self, x=None, y=None):
    self.x = x
    self.y = y
    self.prev = None
    self.next = None
  
  def equals(self, target_x, target_y):
    return target_x == self.x and target_y == self.y
  
  def move(self, delta):
    return (self.x + delta[0], self.y + delta[1])
  
  def __str__(self):
    return f"({self.x},{self.y}) -> {self.next}]"