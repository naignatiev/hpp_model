import matplotlib.pyplot as plt
from PIL import Image
import os
import numpy as np
from base import State


class CeilDrawer:

    def __init__(self):
        self.arrow_params = {
            'head_width': 0.2,
            'head_length': 0.2,
        }

    def draw(self, state: State, i, j, after_collision):
        if after_collision:
            self.draw_after_collision(state, i, j)
        else:
            self.draw_after_spread(state, i, j)

    def draw_after_collision(self, state: State, i, j):
        if state[i][j][0]:
            self.draw_up_ar(i + 0.5, j + 0.5)
        if state[i][j][1]:
            self.draw_right_ar(i + 0.5, j + 0.5)
        if state[i][j][2]:
            self.draw_down_ar(i + 0.5, j + 0.5)
        if state[i][j][3]:
            self.draw_left_ar(i + 0.5, j + 0.5)

    def draw_after_spread(self, state: State, i, j):
        if state[i][j][0]:
            self.draw_up_ar(i + 0.5, j)
        if state[i][j][1]:
            self.draw_right_ar(i, j + 0.5)
        if state[i][j][2]:
            self.draw_down_ar(i + 0.5, j + 1)
        if state[i][j][3]:
            self.draw_left_ar(i + 1, j + 0.5)

    def draw_up_ar(self, x, y):
        plt.arrow(x, y, 0, 0.3, color='black', **self.arrow_params)

    def draw_right_ar(self, x, y):
        plt.arrow(x, y, 0.3, 0, color='black', **self.arrow_params)

    def draw_down_ar(self, x, y):
        plt.arrow(x, y, 0, -0.3, color='black', **self.arrow_params)

    def draw_left_ar(self, x, y):
        plt.arrow(x, y, -0.3, 0, color='black', **self.arrow_params)


class GIF:
    def __init__(self, name, gif_speed):
        self.name = name
        self.gif_speed = gif_speed
        self.frames = []

    def record_frame(self):
        plt.savefig('tmp.png')
        self.frames.append(Image.open('tmp.png'))
        os.remove('tmp.png')

    def save(self):
        self.frames[0].save(f'{self.name}.gif', format='GIF', append_images=self.frames[1:], save_all=True,
                            duration=self.gif_speed, loop=0)


class Scene(CeilDrawer):

    def __init__(self, state: State, gif1=None, gif2=None, gif_speed=None):
        super().__init__()
        self.state = state
        if gif1:
            self.gif1 = GIF(gif1, gif_speed)
        if gif2:
            self.gif2 = GIF(gif2, gif_speed)
        self.bar_max = self._get_eval_bar_max()

    def draw_plots(self, after_collision):
        self.draw_molecular_plot(after_collision)

        if self.gif2:
            self.draw_hist()

    def draw_molecular_plot(self, after_collision):
        self.draw_arrows(after_collision)
        self._draw_fake_molecular_plot_boundaries()
        self.gif1.record_frame()
        plt.clf()

    def draw_hist(self):
        # + 1 bar for correct image
        plt.title('Распределение частиц по вертикалям')
        plt.xlabel('Координата клетки')
        plt.ylabel('Количество частиц на вертикали')
        x = range(self.state.n + 1)
        height = np.concatenate([np.array(self.state).sum(axis=-1).sum(axis=-1), np.array([self.bar_max])])
        plt.bar(x=x, height=height, color=self.state.n * ['red'] + ['white'])
        self.gif2.record_frame()
        plt.clf()

    def draw_arrows(self, after_collision):
        for i in range(self.state.n):
            for j in range(self.state.m):
                self.draw(self.state, i, j, after_collision)

    def _draw_fake_molecular_plot_boundaries(self):
        plt.scatter(x=[-1, -1, self.state.n + 1, self.state.n + 1], y=[-1, self.state.m + 1, -1, self.state.m + 1],
                    color='white')
        plt.axis('off')
        plt.plot([0, 0, self.state.n, self.state.n, 0], [0, self.state.m, self.state.m, 0, 0], linestyle='--',
                 color='black')

    def _get_eval_bar_max(self):
        c = self.state.get_cardinality()
        return min(self.state.m, c) + 1
