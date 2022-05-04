
from controller import Controller

"""
USING RNN unsupervised learning because the controls (or state inputs)
do not/can not affect the input datastream. In other words, there is
nothing the dino can do that will change what any of the next data points
will be, so the dino cannot really navigate the state-space. Thus, reinforcement
learning is either useless or impossible to implement. RNNs are a better choice
for generating a response to the input time-series signal (game state points)
and update its weights by force. 
"""


def build_input_vector(obst, state):
    x = [
        obst.hitbox.right - state['dino'].hitbox.left,
        state['ground_level'] - obst.hitbox.bottom,
        (state['ground_level'] - obst.hitbox.bottom) ** 2,
        obst.hitbox.width,
        obst.hitbox.height,
        state['game_speed'] - obst.base_speed[0]
    ]
    return x


class Perceptron(Controller):

    def __init__(self, scheme: list):
        self.deaths = 0

        self.restart = False
        self.w = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.lr = 0.0001
        self.y = False
        self.triggers = {  # a list of trigger states (unlabeled points) for each output control (jump, duck, etc)
            'pass': [],
            'jump': []
        }
        super().__init__(scheme)

    def run_network(self, x_vector):
        y_vector = sum([self.w[i] * x_vector[i] for i in range(len(x_vector))])
        return y_vector > 0

    def update_weights(self, x_vector, expected=0):
        if x_vector is None or len(x_vector) <= 0:
            return
        for i in range(len(self.w)):
            self.w[i] += expected * self.lr * x_vector[i]  # died from jumping

    # Called by main on every tick.
    # Given a current game state to check for a trigger (like an incoming obstacle).
    # When there is at least one trigger (obstacle) in the frame,
    # the ANN should be consulted for an output control.
    # The moment where a control goes high should be taken as a data point,
    # and the result of that control in a later frame should be taken as the label of that point
    def update(self, state=None):
        if state is None:
            return

        # see about making sure the dino checks weights and jumps in the same tick
        # check if the dino dies, and then pull up the relevant stored trigger point
        if state['playing']:
            # if the dino didn't die, then run the perceptron to update the output controls
            trgd_obst = None
            for obst in state['obstacles']:
                dist = obst.hitbox.right - state['dino'].hitbox.left
                # find the first obstacle that is in front of the dino
                if dist > 0:
                    trgd_obst = obst
                    break
            # cancel when there's no obstacle
            if trgd_obst is None:
                self.y = False
                return
            # get inputs for this tick (point)
            x = build_input_vector(trgd_obst, state)
            # run the network
            self.y = self.run_network(x)
            # capture the next trigger points
            #print(state['on_ground'])
            if state['on_ground']:
                if self.y:
                    #print('captured jump at distance:', x[0])
                    self.triggers['jump'] = x  # if the perceptron made the dino jump, the log a jump point
                else:
                    self.triggers['pass'] = x  # otherwise, always log a no-jump point
        else:
            # update the weights and restart the game if the dino died
            if not state['freeze']:
                self.deaths += 1
                # decide to jump sooner or later:
                # if jump == die going down: jump later
                # if jump == die going up: jump sooner
                # if no-jump == die: jump sooner
                if state['on_ground']:
                    # died going up
                    print('dino died, jump=FALSE, with weights:', self.w)
                    self.update_weights(self.triggers['pass'], 1)
                # if the dino died from not jumping the pass trigger should always be run
                else:
                    print('dino died, jump=TRUE, with weights:', self.w)
                    if state['dino'].dy <= 0:
                        # died going up
                        self.update_weights(self.triggers['jump'], 1)
                    else:
                        # died going down
                        self.update_weights(self.triggers['jump'], -1)
                    #self.update_weights(self.triggers['jump'], -1)
            # reset the triggers and set the restart control high
            self.triggers['jump'].clear()
            self.triggers['pass'].clear()
            self.restart = True

    def source(self, control):
        if control == -1:
            if self.restart:
                self.restart = False
                return True
            else:
                return False
        elif control == 0:
            return self.y
        else:
            return False
