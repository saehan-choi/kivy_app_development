
import gymnasium as gym
import math
import random
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple, deque
from itertools import count

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F


env = gym.make("CartPole-v1", render_mode='human')
env.reset()
while True:
    action = int(input("Action: "))
    if action in (0, 1):
        env.step(action)
        env.render()



# 이거 while True로 잡아버리고 하면될듯안하면 일단계속 진행되게하고 키입력안되면 마지막에 누른 action 계속진행되게 ㅋㅋ





