
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

import gymnasium as gym


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

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


env = gym.make("CartPole-v1", render_mode='human')
env.reset()

n_actions = env.action_space.n
state, info = env.reset()
# print(state)
# [cart position, cart velocity, pole angle, pole angular velocity]
# [-0.04702549 -0.00169586  0.02877673 -0.00429488]

n_observations = len(state)
policy_net = DQN(n_observations, n_actions).to(device)
policy_net.load_state_dict(torch.load('./cartpole_weights/episode_durations_500.pt'))


inp = torch.randn(4).unsqueeze(0).to(device)
# print(torch.argmax(policy_net(inp)).item())
# 이제 됩니다 이걸로 어떻게 구현하면 될듯요
action = torch.argmax(policy_net(inp)).item()


while True:
    
    observation, reward, terminated, truncated, _ = env.step(action)
    
    
    next_state = torch.tensor(observation).to(device)
    
    action = policy_net(next_state)
    print(action)


# while True:
#     action = int(input("Action: "))
#     if action in (0, 1):
#         env.step(action)
#         env.render()
