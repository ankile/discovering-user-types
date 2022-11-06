import numpy as np

class MDP():
    def __init__(self, S, A, T, R, gamma):
        self.S = S
        self.A = A
        self.T = T
        self.R = R
        self.gamma = gamma

        self.V = np.zeros(len(self.S))
        self.policy = np.zeros(len(self.S))
        self.theta = 0.0001
        self.state = self.S[0]

        # sanity checks:
        assert T.shape == (len(self.A), len(self.S), len(self.S)) # action x state x state
        # assert T.sum(axis=0) == 1 # rows of T have to = 1
        assert R.shape == (len(self.S), len(self.A), len(self.S)) # state x action x next_state

    # value iteration is a little funky:
    def updated_action_values(self, state):

        vals = np.zeros(len(self.A))

        for action in self.A:
            to_sum = []
            for p in range(len(self.T[action][state])):
                to_sum.append(self.T[action][state][p] * (self.R[state][action][p] + (self.gamma * self.V[p])))

            vals[action] = sum(to_sum)

        return vals

    def value_iteration(self):
        while True:
            difference = 0
            for state in self.S:
                old_V = self.V[state]
                v = self.updated_action_values(state)

                self.policy[state] = np.argmax(v)
                self.V[state] = np.max(v)

                difference = max(difference, np.abs(old_V - self.V[state]))
            if difference < self.theta:
                break

        print(self.V)

    def solve(self):
        self.value_iteration()

        if len(self.policy) > 0:
            grid = []
            for state in self.S:
                if self.policy[state] == 0:
                    grid.append(u'\u2190 ')
                else:
                    grid.append(u'\u2192 ')

            toDraw = ''.join(grid)
            print(toDraw)

        return

    def reset(self):
        self.state = self.S[0]


class Experiment_1D():

    def __init__(self, length, make_right_prob):
        self.S, self.A, self.T, self.R, self.gamma = self.make_MDP_params(length, make_right_prob)
        self.mdp_1d = MDP(self.S, self.A, self.T, self.R, self.gamma)

    def make_MDP_params(self, length, make_right_prob):
        S = np.arange(length)
        A = np.array((0, 1)) # 0 is left and 1 is right
        gamma = 0.8

        T = np.zeros((2, length, length))

        T[0] = np.diag(np.array([1] + [1 - make_right_prob] * (length-2) + [1])) # 20% chance of staying in the same state unless in state 0 or state l-1

        # Do this more slickly with a np.roll()
        for i in range(1, length-1):
            T[0, i, i-1] = make_right_prob

        T[1] = np.diag(np.array([1 - make_right_prob] * (length-1) + [1])) # 20% chance of staying in the same state unless in state 0 or state l-1

        # Do this more slickly with a np.roll()
        for i in range(0, length-1):
            T[1, i, i+1] = make_right_prob

        R = np.zeros((length, 2, length)) # R is sparse
        R[length-2, 1, length-1] = 10

        return S, A, T, R, gamma

    def myopic(self, gamma):
        self.mdp_1d = MDP(self.S, self.A, self.T, self.R, gamma)

    def confident(self, make_right_prob):
        # probability is LOWER than the "true": UNDERCONFIDENT
        S, A, T, R, gamma = self.make_MDP_params(length = length, make_right_prob = make_right_prob)
        self.mdp_1d = MDP(S, A, T, R, gamma)

    def reward(self, R):
        # TODO:
        pass


if __name__ == '__main__':
    length = 5
    default_prob = 0.8

    # our baseline:
    test = Experiment_1D(length, default_prob)

    # MYOPIC EXPERIMENT RUNS:
    for gamma in np.arange(0.01, 1, 0.1):
        print(f'gamma = {gamma}')
        myopic = test.myopic(gamma = gamma)
        test.mdp_1d.solve()
        print('')

    # UNDERCONFIDENT + OVERCONFIDENT EXPERIMENT RUNS:
    for prob in np.arange(0.01, 1, 0.1):
        print(f'prob = {prob}')
        if prob < default_prob:
            print('UNDERCONFIDENT')

        if prob > default_prob:
            print('OVERCONFIDENT')

        confident = test.confident(make_right_prob = prob)
        test.mdp_1d.solve()
        print('')


    """
    don't hardcode the types of the users in the experiment class
    looking for 5 instantiations of the different classes/experiments
        - world: negative reward floating around -- kevin
        - other 4 correspond to the different users -- eman + me
            - don't worry too much about value iter:
                - still valuable to get this level of generalization down

    11/6/2022:
    - fix value iteration lol
    - ** start moving to 2d world
    - reward agent?? -- wait for response on slack
    - different knobs?
        -

    """
