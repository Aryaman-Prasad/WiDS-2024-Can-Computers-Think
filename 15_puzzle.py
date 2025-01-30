#I had initially attempted this on my own but could not get it to work properly, the runtime was absurdly high and I never got to actually see an output
#To make optimizations, I ended up looking at the code given in the medium and took quite some inspiration from it (and also help from the internet). I just felt I should write this here...

#Takes around 5 mins or so to run and around 70 moves to complete the puzzle
import random
from collections import deque
import time

class FifteenState:
    NUM_CELLS = 16
    FIRST_ROW_SOLVED_STATE = [1, 2, 3, 4, NUM_CELLS, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    SECOND_ROW_SOLVED_STATE = [1, 2, 3, 4, 5, 6, 7, 8, NUM_CELLS, 0, 0, 0, 0, 0, 0, 0]
    ALL_ROWS_SOLVED_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, NUM_CELLS]

    def __init__(self, numbers):
        self.numbers = numbers
        self.rows_solved = self.count_rows_solved()
        self.masked_count = self.count_masked()
        self.terminal = (self.rows_solved == 4 or (self.rows_solved == 2 and self.masked_count == 7) or (self.rows_solved == 1 and self.masked_count == 11))
        self.hash = self.generate_hash()
        self.empty_cell_index = self.numbers.index(self.NUM_CELLS)
        self.value = 0.0

    def mask(self, upper):
        return [0 if x > upper and x != self.NUM_CELLS else x for x in self.numbers]

    def count_rows_solved(self):
        for i in range(self.NUM_CELLS):
            if self.numbers[i] != i + 1:
                if i < 4:
                    return 0
                if i < 8:
                    return 1
                return 2
        return 4

    def count_masked(self):
        return sum(1 for x in self.numbers if x == 0)
    
    def generate_hash(self):
        if self.rows_solved == 0:
            return ','.join(map(str, self.mask(4)))
        elif self.rows_solved == 1:
            return ','.join(map(str, self.mask(8)))
        else:
            return ','.join(map(str, self.numbers))

    def next_state(self, action):
        new_numbers = self.numbers[:]
        new_numbers[self.empty_cell_index], new_numbers[action] = new_numbers[action], self.NUM_CELLS
        return FifteenState(new_numbers)

    def possible_actions(self):
        row = self.empty_cell_index // 4
        col = self.empty_cell_index % 4
        actions = []

        if row > 0:  
            actions.append(4 * (row - 1) + col)
        if row < 3:  
            actions.append(4 * (row + 1) + col)
        if col > 0:  
            actions.append(4 * row + col - 1)
        if col < 3:  
            actions.append(4 * row + col + 1)

        return actions
    
    def show(self):
        for i in range(4):
            print("+----+----+----+----+")
            for j in range(4):
                if self.numbers[4*i + j] == 16:
                    print('|   ', end = ' ')
                elif self.numbers[4*i + j] < 10:
                    print('|  '+str(self.numbers[4*i + j]), end = ' ')
                else:
                    print('| '+str(self.numbers[4*i + j]), end = ' ')
            print('|')
        print('+----+----+----+----+')

class FifteenPuzzle:
    def __init__(self, gamma=0.9, theta=0.1):
        self.states = {}
        self.policy = {}
        self.gamma = gamma
        self.theta = theta

    def reward(self, current_state, next_state):
        if next_state.rows_solved == 4:
            return 100.0
        return (next_state.rows_solved - current_state.rows_solved)

    def generate_states_from(self, final_state):
        work_queue = deque([final_state])
        seen = set()

        while work_queue:
            state = work_queue.popleft()
            self.states[state.hash] = state

            if not state.terminal:
                state.value = random.random()

            for action in state.possible_actions():
                next_state = state.next_state(action)

                if next_state.hash not in seen:
                    self.states[next_state.hash] = next_state
                    self.policy[next_state.hash] = random.choice(next_state.possible_actions())
                    work_queue.append(next_state)
                    seen.add(next_state.hash)

    def calculate_optimal_values(self):
        while True:
            delta = 0
            for _, state in self.states.items():
                if state.terminal:
                    continue
                old_value = state.value
                action_values = []
                for action in state.possible_actions():
                    if state.rows_solved <= state.next_state(action).rows_solved:
                        next_state = state.next_state(action)
                        action_value = (
                            self.reward(state, next_state) +
                            self.gamma * self.states[next_state.hash].value
                        )
                        action_values.append(action_value)

                state.value = max(action_values)
                delta = max(delta, abs(old_value - state.value))
            if delta < self.theta:
                break

    def calculate_optimal_policy(self):
        for state_hash, state in self.states.items():
            if state.terminal:
                continue
            action_values = {}
            for action in state.possible_actions():
                if state.rows_solved <= state.next_state(action).rows_solved:
                    action_values[action] = self.reward(state, state.next_state(action)) + self.gamma * self.states[state.next_state(action).hash].value
            best_action = max(action_values, key=action_values.get)
            self.policy[state_hash] = best_action

    def display(self, initial_state):
        current_state = initial_state
        current_state.show()
        print('T = 0')
        t = 0
        time.sleep(1)
        while current_state.rows_solved != 4:
            action = self.policy.get(current_state.hash)
            if action is not None:
                next_state = current_state.next_state(action)
            else:
                next_state = current_state.next_state(random.choice(current_state.possible_actions))
            current_state = next_state
            current_state.show()
            t += 1
            print(f'T = {t}')
            time.sleep(1)

    def generate_random_puzzle(self):
        numbers = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        for _ in range(10000):
            numbers = FifteenState(numbers).next_state(random.choice(FifteenState(numbers).possible_actions())).numbers
        return FifteenState(numbers)
    
    def run(self):
        self.generate_states_from(FifteenState(FifteenState.ALL_ROWS_SOLVED_STATE))
        self.calculate_optimal_values()
        self.calculate_optimal_policy()
        x = self.generate_random_puzzle()
        self.display(x)

puzzle = FifteenPuzzle()
puzzle.run()
