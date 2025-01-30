#I did this after completing the 15-puzzle project lmao don't ask why even I don't know...anyways, the heatmap is fairly accurate I feel, could probably get better if I run it for longer (like more iterations)
#Might take a minute or two to run
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math

def poisson(l):
    return int(np.random.poisson(l))

def possible_next_states(state):
    l = []
    for i in[-5,-4,-3,-2,-1,0,1,2,3,4,5]:
        if state[0]>=i and state[1]>=-i:
            if state[1]+i<=20 and state[0]-i<=20:
                l.append([state[0]-i, state[1]+i])
            elif state[1]+i>20 and state[0]-i<=20:
                l.append([state[0]-i, 20])
            elif state[1]+i<=20 and state[0]-i>20:
                l.append([20, state[1]+i])
    return l

def chance(n, l):
    prob = 0
    for i in range(int(n+1)):
        prob += (l**i)*(math.e**(-l))/math.factorial(i)
    return prob

def policy_iteration(policy, states, values):
  while True:
    delta = 0.0
    for state in states:
        a_l = {}
        v = values[state[0]][state[1]]
        for s in possible_next_states(state):
            a = max(state[0] - s[0], s[1] - state[1])
            req_a,req_b,ret_a,ret_b = 0,0,0,0
            for _ in range(200):
                req_a += poisson(3)
                req_b += poisson(4)
                ret_a += poisson(3)
                ret_b += poisson(2)
            req_a /= 200
            req_b /= 200
            ret_a /= 200
            ret_b /= 200
            a_l[a] = (chance(s[0]+ret_a, 3) * chance(s[1]+ret_b, 4)) * (((req_a + req_b) - (0.2 * a)) + 0.9 * values[s[0]][s[1]])
        best_a = max(a_l, key = a_l.get)
        values[state[0]][state[1]] = a_l[best_a]
        policy[state[0]][state[1]] = best_a
        delta = max(delta, np.abs(v - values[state[0]][state[1]]))
    if delta < 4.5:
        break
  return policy

policy = np.random.randint(low = 0, high = 1, size = (21, 21))
values = np.random.random(size = (21, 21))
states = []
for i in range(21):
    for j in range(21):
        states.append([i,j])
actions = [-5,-4,-3,-2,-1,0,1,2,3,4,5]
req_a,req_b,ret_a,ret_b = poisson(3),poisson(4),poisson(3),poisson(2)
for i in range(5):
    policy = policy_iteration(policy, states, values)
print(chance(3, 3))
sns.heatmap(policy)
plt.show()