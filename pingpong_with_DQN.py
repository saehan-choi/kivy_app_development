import math
import random
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple, deque
from itertools import count
from pingpong import PongEnv

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F



class ReplayMemory(object):

    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        """Save a transition"""
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


class DQN(nn.Module):

    def __init__(self, n_observations, n_actions):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(n_observations, 128)
        self.layer2 = nn.Linear(128, 128)
        self.layer3 = nn.Linear(128, n_actions)

    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).
    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return self.layer3(x)

    
# epsilon greedy 
def select_action(state):
    global steps_done
    sample = random.random()
    eps_threshold = EPS_END + (EPS_START - EPS_END) * \
        math.exp(-1. * steps_done / EPS_DECAY)
    steps_done += 1
    if sample > eps_threshold:
        with torch.no_grad():
            return policy_net(state).max(1)[1].view(1, 1)
    else:
        return torch.tensor([[random.choice(env.action_space)]], device=device, dtype=torch.long)


def optimize_model():
    if len(memory) < BATCH_SIZE:
        return
    transitions = memory.sample(BATCH_SIZE)
    batch = Transition(*zip(*transitions))

    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                          batch.next_state)), device=device, dtype=torch.bool)    
    non_final_next_states = torch.cat([s for s in batch.next_state
                                                if s is not None])
    # print(non_final_mask) -> tensor([ True,  True,  True,  True,  True,  True,  True,  True -> boolean의 batchsize로 묶은것들을 나타냄
    # print(non_final_next_states) -> tensor([[-3.8601e-02, -4.3774e-01,  2.3463e-02,  5.7385e-01], [ 4.0245e-02,  5.5229e-01,  1.3867e-02, -8.0089e-01] state를 batchsize로 묶은 tensor를 나타냄
    # non_final_mask는 batch사이즈의 숫자대로 나오고 non_final_next_states는 next_state가 없으면 저장을 안함!

    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)

    state_action_values = policy_net(state_batch).gather(1, action_batch)
    next_state_values = torch.zeros(BATCH_SIZE, device=device)

    with torch.no_grad():
        next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0]

    # a = torch.tensor([0,0,0,0,0,        0,0,0,0,0], dtype=torch.float)
    # b = torch.tensor([True,True,True,True,True,           False,True,True,True,True], dtype=torch.bool)
    # a[b] = torch.tensor([5.6, 5.3, 5.2, 5.4, 5.1,  1.2, 1.5, 1.8, 1.9], dtype=torch.float)
    # results -> tensor([5.6000, 5.3000, 5.2000, 5.4000, 5.1000, 0.0000, 1.2000, 1.5000, 1.8000, 1.9000])

    expected_state_action_values = (next_state_values * GAMMA) + reward_batch
    criterion = nn.SmoothL1Loss()
    # criterion(pred, target)
    loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))
    optimizer.zero_grad()
    loss.backward()
    torch.nn.utils.clip_grad_value_(policy_net.parameters(), 100)
    optimizer.step()


if __name__ == '__main__':

    env = PongEnv()

    BATCH_SIZE = 128
    GAMMA = 0.99
    EPS_START = 0.9
    EPS_END = 0.05
    EPS_DECAY = 1000
    TAU = 0.005
    LR = 1e-4

    n_actions = len(env.action_space)
    steps_done = 0
    num_episodes = 1000

    # if gpu is to be used
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    Transition = namedtuple('Transition',
                            ('state', 'action', 'next_state', 'reward'))


    # state = [left_pad_y, right_pad_y, ball_x, ball_y, ball_dx, ball_dy]
    state = env.reset()

    # print(state)
    # [cart position, cart velocity, pole angle, pole angular velocity]
    # [-0.04702549 -0.00169586  0.02877673 -0.00429488]
    n_observations = len(state)

    policy_net = DQN(n_observations, n_actions).to(device)
    target_net = DQN(n_observations, n_actions).to(device)
    target_net.load_state_dict(policy_net.state_dict())

    optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)
    memory = ReplayMemory(10000)


