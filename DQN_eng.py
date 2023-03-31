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




# 환경 생성
env = gym.make("CartPole-v1")

# set up matplotlib
is_ipython = 'inline' in matplotlib.get_backend()
if is_ipython:
    from IPython import display

# plt를 지속적으로 업데이트할 수 있는 함수임.
plt.ion()

# if gpu is to be used
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

    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).
    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return self.layer3(x)

# BATCH_SIZE is the number of transitions sampled from the replay buffer
# GAMMA is the discount factor as mentioned in the previous section
# EPS_START is the starting value of epsilon
# EPS_END is the final value of epsilon
# EPS_DECAY controls the rate of exponential decay of epsilon, higher means a slower decay
# TAU is the update rate of the target network
# LR is the learning rate of the AdamW optimizer

BATCH_SIZE = 128
GAMMA = 0.99
EPS_START = 0.9
EPS_END = 0.05
EPS_DECAY = 1000
TAU = 0.005
LR = 1e-4

# Get number of actions from gym action space
n_actions = env.action_space.n
# Get the number of state observations
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
            # t.max(1) will return the largest column value of each row.
            # second column on max result is index of where max element was
            # found, so we pick action with the larger expected reward.
            
            # action index가 나옴 -> 1차원을 unsqueeze(0) 하는것과 같다고 보면됩니다.
            # return값 -> tensor([[1]], device='cuda:0') 이렇게 나옵니다.
            return policy_net(state).max(1)[1].view(1, 1)

    # target_net(non_final_next_states).max(1)[0] -> action value
    # values=tensor([-0.0114, -0.0129, -0.0129, -0.0136, -0.0136, -0.0133, -0.0105, -0.0117,
    #         -0.0134, -0.0115, -0.0131, -0.0140, -0.0125, -0.0129, -0.0134, -0.0115], device='cuda:0', grad_fn=<MaxBackward0>)

    # target_net(non_final_next_states).max(1)[1] -> action index
    #        device='cuda:0', grad_fn=<MaxBackward0>),
    # indices=tensor([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], device='cuda:0')

    else:
        # eps_threshold는 지속적으로 steps_done이 늘어날수록 줄어든다. 따라서 처음은 randomly 하게 행동하다가
        # 시간이 지날수록 greedy하게 행동한다.
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
    # Take 100 episode averages and plot them too
    if len(durations_t) >= 100:
        means = durations_t.unfold(0, 100, 1).mean(1).view(-1)
        means = torch.cat((torch.zeros(99), means))
        plt.plot(means.numpy())

    plt.pause(0.001)  # pause a bit so that plots are updated
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
    # Transpose the batch (see https://stackoverflow.com/a/19343/3343043 for
    # detailed explanation). This converts batch-array of Transitions
    # to Transition of batch-arrays.
    batch = Transition(*zip(*transitions))

    # Compute a mask of non-final states and concatenate the batch elements
    # (a final state would've been the one after which simulation ended)
    # s is not None -> 두 변수 옆에 이것을 선언해줌으로서 non final일때만 그 상태값들을 가져옴!

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

    # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
    # columns of actions taken. These are the actions which would've been taken
    # for each batch state according to policy_net
    state_action_values = policy_net(state_batch).gather(1, action_batch)

    # Compute V(s_{t+1}) for all next states.
    # Expected values of actions for non_final_next_states are computed based
    # on the "older" target_net; selecting their best reward with max(1)[0].
    # This is merged based on the mask, such that we'll have either the expected
    # state value or 0 in case the state was final.
    next_state_values = torch.zeros(BATCH_SIZE, device=device)

    # 여기서 하고자 하는것은 단순하다. next_state가 None이 아닌, 즉 next_state가 남아있는 상태를 target network로 집어넣어서
    # 결과값을 얻은 다음 현재의 상태와 미래의 state action value를 최소화 하는 방향으로 학습한다. 
    # 따라서 미래의 보상값이 최대한 좋은 방향으로 현재의 값을 return 하는것이다.
    with torch.no_grad():
        next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0]

    # a = torch.tensor([0,0,0,0,0,        0,0,0,0,0], dtype=torch.float)
    # b = torch.tensor([True,True,True,True,True,           False,True,True,True,True], dtype=torch.bool)
    # a[b] = torch.tensor([5.6, 5.3, 5.2, 5.4, 5.1,  1.2, 1.5, 1.8, 1.9], dtype=torch.float)
    # results -> tensor([5.6000, 5.3000, 5.2000, 5.4000, 5.1000, 0.0000, 1.2000, 1.5000, 1.8000, 1.9000])

    # Compute the expected Q values
    expected_state_action_values = (next_state_values * GAMMA) + reward_batch

    # Compute Huber loss
    criterion = nn.SmoothL1Loss()
    # criterion(pred, target) 입니다.
    loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))

    # Optimize the model
    optimizer.zero_grad()
    loss.backward()
    # In-place gradient clipping
    torch.nn.utils.clip_grad_value_(policy_net.parameters(), 100)
    optimizer.step()

if torch.cuda.is_available():
    num_episodes = 600
else:
    num_episodes = 50

for i_episode in range(num_episodes):
    # Initialize the environment and get it's state
    state, info = env.reset()
    # print(state)
    # [cart position, cart velocity, pole angle, pole angular velocity]
    # [-0.04702549 -0.00169586  0.02877673 -0.00429488]

    state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
    # print(state) -> tensor([[-0.0311, -0.0486, -0.0449, -0.0446]], device='cuda:0')  이거 하나나옴
    for t in count():
        action = select_action(state)
        observation, reward, terminated, truncated, _ = env.step(action.item())
        # observation - action후 상태
        # reward - action후 보상
        # terminated - 에피소드 종료여부
        # truncated - 최대시간 단계에 도달해서 강제로 종료여부

        reward = torch.tensor([reward], device=device)
        done = terminated or truncated

        if terminated:
            next_state = None
        else:
            # print(observation) -> action후 현재 state  -> [cart position, cart velocity, pole angle, pole angular velocity]
            next_state = torch.tensor(observation, dtype=torch.float32, device=device).unsqueeze(0)

        # Store the transition in memory
        memory.push(state, action, next_state, reward)

        # Move to the next state
        state = next_state

        # Perform one step of the optimization (on the policy network)
        optimize_model()

        # Soft update of the target network's weights
        # θ′ ← τ θ + (1 −τ )θ′
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



