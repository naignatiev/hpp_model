from draw import Scene
from base import State
from tqdm import tqdm


class HPP:
    def __init__(self, state: State, gif1=None, gif2=None, gif_speed=None):
        self.state = state
        self.scene = Scene(state, gif1, gif2, gif_speed)

    def run(self, n_times):
        for _ in tqdm(range(n_times)):
            self.scene.draw_plots(after_collision=True)
            self.__spread()
            self.scene.draw_plots(after_collision=False)
            self.__collision()
        self.scene.gif1.save()
        self.scene.gif2.save()

    def __spread(self):
        new_s = State(self.state.n, self.state.m)
        for i in range(self.state.n):
            for j in range(self.state.m):
                if self.state[i][j][0]:  # up
                    if j < self.state.m - 1:
                        new_s[i][j + 1][0] = self.state[i][j][0]
                    else:
                        new_s[i][0][0] = self.state[i][j][0]
                if self.state[i][j][1]:  # right
                    if i < self.state.n - 1:
                        new_s[i + 1][j][1] = self.state[i][j][1]
                    else:
                        new_s[0][j][1] = self.state[i][j][1]
                if self.state[i][j][2]:  # down
                    if j > 0:
                        new_s[i][j - 1][2] = self.state[i][j][2]
                    else:
                        new_s[i][self.state.m - 1][2] = self.state[i][j][2]
                if self.state[i][j][3]:  # left
                    if i > 0:
                        new_s[i - 1][j][3] = self.state[i][j][3]
                    else:
                        new_s[self.state.n - 1][j][3] = self.state[i][j][3]
        self.state = new_s
        self.scene.state = new_s

    def __collision(self):
        for i in range(self.state.n):
            for j in range(self.state.m):
                if self.state[i][j] == [1, 0, 1, 0]:
                    self.state[i][j] = [0, 1, 0, 1]
                elif self.state[i][j] == [0, 1, 0, 1]:
                    self.state[i][j] = [1, 0, 1, 0]

