import torch
import random
import numpy as np
from snake_game import SnakeGame
from model import Linear_QNet, QTrainer
from collections import deque

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
  def __init__(self):
    self.game_count = 0
    self.epsilon = 0  # randomness
    self.gamma = 0.9  # discount rate
    self.memory = deque(maxlen=MAX_MEMORY)
    self.model = Linear_QNet(11, 256, 3)
    self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

  def get_state(self, game):
    head = game.snake.head
    point_u = (head.x, head.y + 1)
    point_r = (head.x + 1, head.y)
    point_d = (head.x, head.y - 1)
    point_l = (head.x - 1, head.y)

    dir_u = game.snake.heading == 0
    dir_r = game.snake.heading == 1
    dir_d = game.snake.heading == 2
    dir_l = game.snake.heading == 3

    state = [
      # Danger straight ahead
      (dir_u and game.snake.isCollision(point_u[0], point_u[1])) or
      (dir_r and game.snake.isCollision(point_r[0], point_r[1])) or
      (dir_d and game.snake.isCollision(point_d[0], point_d[1])) or
      (dir_l and game.snake.isCollision(point_l[0], point_l[1])),

      # Danger to the right
      (dir_l and game.snake.isCollision(point_u[0], point_u[1])) or
      (dir_u and game.snake.isCollision(point_r[0], point_r[1])) or
      (dir_r and game.snake.isCollision(point_d[0], point_d[1])) or
      (dir_d and game.snake.isCollision(point_l[0], point_l[1])),

      # Danger to the left
      (dir_r and game.snake.isCollision(point_u[0], point_u[1])) or
      (dir_d and game.snake.isCollision(point_r[0], point_r[1])) or
      (dir_l and game.snake.isCollision(point_d[0], point_d[1])) or
      (dir_u and game.snake.isCollision(point_l[0], point_l[1])),

      # Move direction
      dir_l,
      dir_r,
      dir_u,
      dir_d,

      # Food location
      game.snake.food_x < game.snake.head.x,  # food left
      game.snake.food_x > game.snake.head.x,  # food right
      game.snake.food_y < game.snake.head.y,  # food up
      game.snake.food_y > game.snake.head.y,  # food down
    ]

    return np.array(state, dtype=int)

  def remember(self, state, action, reward, next_state, done):
    # automatically popleft if MAX_MEMORY is reached
    self.memory.append((state, action, reward, next_state, done))

  def train_long_memory(self):
    if len(self.memory) > BATCH_SIZE:
      mini_sample = random.sample(self.memory, BATCH_SIZE)
    else:
      mini_sample = self.memory

      states, actions, rewards, next_states, dones = zip(*mini_sample)
      self.trainer.train_step(states, actions, rewards, next_states, dones)
      # for state, action, reward, nexrt_state, done in mini_sample:
      #    self.trainer.train_step(state, action, reward, next_state, done)

  def train_short_memory(self, state, action, reward, next_state, done):
    self.trainer.train_step(state, action, reward, next_state, done)

  def get_action(self, state):
    # random moves: tradeoff exploration / exploitation
    self.epsilon = 80 - self.game_count
    if random.randint(0, 200) < self.epsilon:
      return random.randint(0, 2)
    state0 = torch.tensor(state, dtype=torch.float)
    prediction = self.model(state0)
    return torch.argmax(prediction).item()


def train():
  # plot_scores = []
  # plot_mean_scores = []
  # total_score = 0
  record = 0
  agent = Agent()
  game = SnakeGame()

  while True:
    # get old state
    state_old = agent.get_state(game)

    # get move
    final_move = agent.get_action(state_old)

    # perform move and get new state
    reward, done, score = game.step(final_move)
    state_new = agent.get_state(game)

    # train short memory
    agent.train_short_memory(state_old, final_move, reward, state_new, done)

    # remember
    agent.remember(state_old, final_move, reward, state_new, done)

    if done:
      # train long memory, plot result
      game.resetGame()
      agent.game_count += 1
      agent.train_long_memory()

      if score > record:
        record = score
        agent.model.save()

      print('Game', agent.game_count, 'Score', score, 'Record:', record)

      # plot_scores.append(score)
      # total_score += score
      # mean_score = total_score / agent.game_count
      # plot_mean_scores.append(mean_score)
      # plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()
