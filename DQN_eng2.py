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

env = gym.make("CartPole-v1")

is_ipython = 'inline' in matplotlib.get_backend()
if is_ipython:
    from IPython import display

# plt를 지속적으로 업데이트할 수 있는 함수
plt.ion()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))


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

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return self.layer3(x)

BATCH_SIZE = 128
GAMMA = 0.99
EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 1000
TAU = 0.005
LR = 1e-4

n_actions = env.action_space.n
state, info = env.reset()
# print(state)
# [cart position, cart velocity, pole angle, pole angular velocity]
# [-0.04702549 -0.00169586  0.02877673 -0.00429488]

n_observations = len(state)

policy_net = DQN(n_observations, n_actions).to(device)
target_net = DQN(n_observations, n_actions).to(device)
target_net.load_state_dict(policy_net.state_dict())

optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)
memory = ReplayMemory(10000)

steps_done = 0

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

    # target_net(non_final_next_states).max(1)[0] -> action value
    # values=tensor([-0.0114, -0.0129, -0.0129, -0.0136, -0.0136, -0.0133, -0.0105, -0.0117,
    #         -0.0134, -0.0115, -0.0131, -0.0140, -0.0125, -0.0129, -0.0134, -0.0115], device='cuda:0', grad_fn=<MaxBackward0>)

    # target_net(non_final_next_states).max(1)[1] -> action index
    #        device='cuda:0', grad_fn=<MaxBackward0>),
    # indices=tensor([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], device='cuda:0')

    else:
        return torch.tensor([[env.action_space.sample()]], device=device, dtype=torch.long)

episode_durations = []

def plot_durations(show_result=False):
    plt.figure(1)
    durations_t = torch.tensor(episode_durations, dtype=torch.float)
    if show_result:
        plt.title('Result')
    else:
        plt.clf()
        plt.title('Training...')
    plt.xlabel('Episode')
    plt.ylabel('Duration')
    plt.plot(durations_t.numpy())
    if len(durations_t) >= 100:
        means = durations_t.unfold(0, 100, 1).mean(1).view(-1)
        means = torch.cat((torch.zeros(99), means))
        plt.plot(means.numpy())

    plt.pause(0.001)
    if is_ipython:
        if not show_result:
            display.display(plt.gcf())
            display.clear_output(wait=True)
        else:
            display.display(plt.gcf())

def optimize_model():
    if len(memory) < BATCH_SIZE:
        return
    transitions = memory.sample(BATCH_SIZE)
    # print(transitions) -> Transition(state=tensor([[-0.0450, -0.2008, -0.0561,  0.1227]], device='cuda:0'), action=tensor([[1]], device='cuda:0'), next_state=tensor([[-0.0490, -0.0049, -0.0536, -0.1872]], device='cuda:0'), reward=tensor([1.], device='cuda:0')), ...
    # print(len(transitions)) -> 128
    batch = Transition(*zip(*transitions))

    #  print(batch)
    #  Transition(state=(tensor([[-0.0942, -0.4061,  0.0552,  0.7115]], device='cuda:0'), tensor([[ 0.0569,  0.7496, -0.0704, -1.1774]], device='cuda:0'), tensor([[-0.0302,  0.5477,  0.0814, -0.2728]], device='cuda:0'), tensor([[ 0.0908,  0.7517, -0.1238, -1.2293]], device='cuda:0'), tensor([[ 0.0497,  0.8188, -0.1053, -1.2557]], device='cuda:0'), tensor([[-0.0192,  0.3515, 
    #  0.0760,  0.0444]], device='cuda:0'), tensor([[-0.0832, -0.2011,  0.0404,  0.1999]], device='cuda:0'), tensor([[-0.0852, -0.0136,  0.0361,  0.0745]], device='cuda:0'), tensor([[-0.1086,  0.5602,  0.1007, -0.5514]], device='cuda:0'), tensor([[-0.0404,  0.1599,  0.0764,  0.2607]], device='cuda:0'), tensor([[ 0.0048,  0.3588,  0.0107, -0.5763]], device='cuda:0'), tensor([[ 0.1026, -0.2010, -0.1999, -0.2318]], device='cuda:0'), tensor([[-0.0855, -0.2092,  0.0376,  0.3784]], device='cuda:0'), tensor([[ 0.0661,  1.0151, -0.1304, -1.5794]], device='cuda:0'), tensor([[ 0.1399,  0.5627, -0.2059, -1.0836]], device='cuda:0'), tensor([[ 0.0163, -0.0273, -0.0011, -0.0482]], device='cuda:0'), tensor([[-0.0013,  0.7394,  0.0724, -0.4909]], device='cuda:0'), tensor([[ 0.1028,  1.0185, -0.1886, -1.6688]], device='cuda:0'), tensor([[ 0.0864,  0.8218, -0.1620, -1.3301]], device='cuda:0'), tensor([[ 0.0308,  0.6162, -0.0721, -1.0144]], device='cuda:0'), tensor([[-0.0635, -0.5907,  0.0153,  0.7706]], device='cuda:0'), tensor([[-0.0914, -0.0078,  0.0473, -0.0523]], device='cuda:0'), tensor([[ 1.1959e-02,  5.5374e-01, -8.1690e-04, -8.6561e-01]], device='cuda:0'), tensor([[-0.1159,  0.3668,  0.1065, -0.2941]], device='cuda:0'), tensor([[-0.0999, -0.0106,  0.0566,  0.0094]], device='cuda:0'), tensor([[ 0.0151,  0.0260, -0.0443, -0.0275]], device='cuda:0'), tensor([[ 0.0431,  0.8122, -0.0923, -1.3288]], device='cuda:0'), tensor([[ 0.0993, -0.0138, -0.1699, -0.3500]], device='cuda:0'), tensor([[ 0.0985, -0.0037, -0.2045, -0.5803]], device='cuda:0'), tensor([[-0.0358, -0.3959, -0.0194,  0.4852]], device='cuda:0'), tensor([[ 0.0162, -0.0378,  0.0205, -0.0103]], device='cuda:0'), tensor([[-0.0135,  0.3597,  0.0402, -0.5980]], device='cuda:0'), tensor([[ 0.0155, -0.2332,  0.0203,  0.2888]], device='cuda:0'), tensor([[-0.0160, -0.3970, -0.0453,  0.5107]], device='cuda:0'), tensor([[-0.0122,  0.5455,  0.0769, -0.2234]], device='cuda:0'), tensor([[ 0.0032,  0.2295, -0.0386, -0.2857]], device='cuda:0'), tensor([[-0.0118, -0.0083, -0.0492, -0.0426]], device='cuda:0'), tensor([[ 0.0593,  1.0083, -0.1189, -1.6489]], device='cuda:0'), tensor([[-0.0120, -0.2026, -0.0500,  0.2342]], device='cuda:0'), tensor([[ 0.0370,  0.5589, -0.0413, -0.9456]], device='cuda:0'), tensor([[ 0.1805,  0.9339, -0.0546, -0.7694]], device='cuda:0'), tensor([[ 0.1468,  0.5542, -0.1925, -1.0515]], device='cuda:0'), tensor([[ 0.1293,  0.5416, -0.0306, -0.1369]], device='cuda:0'), tensor([[-0.0437, -0.5907, -0.0096,  0.7718]], device='cuda:0'), tensor([[ 0.0078,  0.4252, -0.0443, -0.5903]], device='cuda:0'), tensor([[ 0.2631,  1.3282, -0.1303, -1.4533]], device='cuda:0'), tensor([[-0.0501, -0.0322,  0.0635,  0.4853]], device='cuda:0'), tensor([[ 0.0873,  0.9372, -0.0943, -1.4658]], device='cuda:0'), tensor([[ 0.1146,  0.7364, -0.0222, -0.4225]], device='cuda:0'), tensor([[ 0.0026,  0.0339, -0.0390,  0.0191]], device='cuda:0'), tensor([[-0.1147, -0.2139,  0.0932,  0.4834]], device='cuda:0'), tensor([[ 0.2897,  1.1349, -0.1594, -1.2040]], device='cuda:0'), tensor([[ 0.0131,  0.1577,  0.0267, -0.3113]], device='cuda:0'), tensor([[ 0.1401,  0.7371, -0.0334, 
    #             action=(tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]], device='cuda:0'), tensor([[1]], 
    # device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[0]], device='cuda:0'), tensor([[1]]    
    #             next_state ...
    #             reward ...

    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                          batch.next_state)), device=device, dtype=torch.bool)    
    non_final_next_states = torch.cat([s for s in batch.next_state
                                                if s is not None])

    # print(non_final_mask) -> tensor([ True,  True,  True,  True,  True,  True,  True,  True -> boolean의 batchsize로 묶은것들을 나타냄
    # print(non_final_next_states) -> tensor([[-3.8601e-02, -4.3774e-01,  2.3463e-02,  5.7385e-01], [ 4.0245e-02,  5.5229e-01,  1.3867e-02, -8.0089e-01] state를 batchsize로 묶은 tensor를 나타냄
    # non_final_mask는 batch사이즈의 숫자대로 나오고 non_final_next_states는 next_state가 없으면 저장을 안함!

    state_batch = torch.cat(batch.state)
    # torch.Size([128, 4])
    action_batch = torch.cat(batch.action)
    # torch.Size([128, 1])
    reward_batch = torch.cat(batch.reward)
    # torch.Size([128])

    state_action_values = policy_net(state_batch).gather(1, action_batch)
    
    print(policy_net(state_batch).gather(1, action_batch))
    
    # >>> t = torch.tensor([[1, 2], [3, 4]])
    # >>> torch.gather(t, 1, torch.tensor([[0, 0], [1, 0]]))
    # tensor([[ 1,  1],
    #         [ 4,  3]])

    # state_action_values.size() -> torch.Size([128, 1]) 입니다.
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

if torch.cuda.is_available():
    num_episodes = 600
else:
    num_episodes = 50

for i_episode in range(num_episodes):
    state, info = env.reset()

    print(info)
    # [cart position, cart velocity, pole angle, pole angular velocity]
    # [-0.04702549 -0.00169586  0.02877673 -0.00429488]
    state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
    for t in count():
        action = select_action(state)
        observation, reward, terminated, truncated, _ = env.step(action.item())
        reward = torch.tensor([reward], device=device)
        done = terminated or truncated

        if terminated:
            next_state = None
        else:
            # print(observation) -> action후 state  -> [cart position, cart velocity, pole angle, pole angular velocity]
            next_state = torch.tensor(observation, dtype=torch.float32, device=device).unsqueeze(0)

        memory.push(state, action, next_state, reward)
        state = next_state
        optimize_model()

        target_net_state_dict = target_net.state_dict()
        policy_net_state_dict = policy_net.state_dict()

        for key in policy_net_state_dict:
            target_net_state_dict[key] = policy_net_state_dict[key]*TAU + target_net_state_dict[key]*(1-TAU)
        target_net.load_state_dict(target_net_state_dict)
        if done:
            episode_durations.append(t + 1)
            
            if episode_durations[-1] > 400:
                torch.save(policy_net_state_dict, f'./cartpole_weights/episode_durations_{episode_durations[-1]}.pt')
            
            plot_durations()
            break

print('Complete')
plot_durations(show_result=True)
plt.ioff()
plt.show()