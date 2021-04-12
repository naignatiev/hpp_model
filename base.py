from draw import *
import numpy as np


class State(list):
    def __init__(self, n, m):
        self.n = n
        self.m = m
        super().__init__([[[0, 0, 0, 0] for _ in range(self.n)] for _ in range(self.m)])

    def get_cardinality(self):
        return np.array(self).sum()


class RandomInit:
    @staticmethod
    def uniform(state: State, p):
        RandomInit.area_uniform(state, p, 0, state.n)

    @staticmethod
    def uniform_2(state: State, p1, p2):
        RandomInit.area_uniform(state, int(p1 / 2), 0, int(0.4 * state.n))
        RandomInit.area_uniform(state, p2, int(0.4 * state.n), int(0.6 * state.n))
        RandomInit.area_uniform(state, int(p1 / 2), int(0.6 * state.n), state.n)

    @staticmethod
    def circle(state: State, center_x, center_y, r, p_sphere, p_env):
        RandomInit.area_uniform(state, p_env, 0, state.n)
        corr_p_sphere = p_sphere
        sphere_dots = []
        for i in range(state.n):
            for j in range(state.m):
                if (i - center_x)**2 + (j - center_y)**2 < r**2:
                    corr_p_sphere -= sum(state[i][j])
                    sphere_dots.append((i, j))
        RandomInit.sphere_uniform(state, sphere_dots, corr_p_sphere)

    @staticmethod
    def area_uniform(state: State, p: int, x0: int, x1: int):
        # только для вертикальных
        dx = (x1 - x0)
        for ijk in np.random.permutation(4 * dx * state.m)[:p]:
            i = int(ijk / 4) % dx
            j = int(ijk / (4 * dx))
            k = ijk % 4
            state[x0 + i][j][k] = 1

    @staticmethod
    def sphere_uniform(state: State, sphere_dots: list, p: int):
        for ijk in np.random.permutation(4 * len(sphere_dots))[:p]:
            i, j = sphere_dots[int(ijk / 4)]
            k = ijk % 4
            state[i][j][k] = 1
