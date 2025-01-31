#Doing this after completing the 15-puzzle and car rental problem...just sayin hehe

#My output more or less matches with the one given in the book (atleast the 3 peaks do)
# but there's some other peaks as well for some reason (I suppose this isn't perfect)

#I'm not very sure why the algorithm considers the ideal policy as it is,
# I think it has something to do with the fact that p(head)<0.5 so sometimes, 
# instead of betting smaller amounts and gradually increasing the capital, 
# chances of success might be better if we bet the maximum amount in one go.

import numpy as np
import matplotlib.pyplot as plt

def generate_states(p):
    states = {0 : {0 : {0 : [1,0], 1 : [1,0]}}}
    for s in range(1, 100):
        states[s] = {}
        for a in range(1, 1 + min(s, 100 - s)):
            states[s][a] = {}
        for a in range(1, 1 + min(s, 100 - s)):
            states[s][a][0] = [1-p, s - a]
            states[s][a][1] = [p, s + a]
            if s + a == 100:
                states[s][a][1] = [p, 100]
            if s == a:
                states[s][a][0] = [1-p, 0]
    states[100] = {0 : {0 : [1,100], 1 : [1,100]}}
    return states

def value_iteration(states, p, values, gamma=1e-20, theta=1e-25):
    policy = {}
    while True:
        delta = 0
        for state in states:
            if state == 0 or state == 100:
                continue
            v = values[state]
            v_l = {}
            for a in states[state]:
                v_l[a] = p*(values[state+a] + gamma*values[state+a]) + (1-p)*(values[state-a] + gamma*values[state-a])
            best_a = max(v_l, key = v_l.get)
            values[state] = v_l[best_a]
            policy[state] = best_a
            delta = max(delta, np.abs(v - values[state]))
        if delta < theta:
            break
    return policy

p = 0.4
states = generate_states(p)
values = {}
for i in range(101):
    values[i] = 0
values[100] = 1
policy = value_iteration(states, p, values)
print(policy)
plt.plot(policy.values())
plt.show()