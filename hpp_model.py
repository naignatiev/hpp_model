from time import sleep
import os
import numpy as np


class System:
    
    def __init__(self, n = 100, m = 100, tick_dur = 0.5, random_type='uniform', p=None, p2=None):
        self.n = n
        self.m = m
        self.tick_dur = tick_dur
        self.s = [[[0, 0, 0, 0] for _ in range(n)] for _ in range(m)]
        #--TEST-----------------
        self.__init_random(random_type, p, p2)
        #-----------------------
        self.ceil_drawer = CeilDrawer()
        self._gif_arr = []
        self._gif2_arr = []
        
    def run(self, n_times=10, only_spread=False, make_gif=False, gif_name='system', gif_speed=300):
        for i in range(n_times):
            self.__draw(before_spread=True, make_gif=make_gif, gif_name=gif_name, shot_n= i * 2)
            self.__spread()
            if not make_gif:
                sleep(self.tick_dur)
            if not only_spread:
                self.__draw(before_spread=False, make_gif=make_gif, gif_name=gif_name, shot_n= i * 2 + 1)
                self.__collision()
                if not make_gif:
                    sleep(self.tick_dur)
                    
#         self.__draw(before_spread=False, make_gif=save_fig, fig_name=fig_name, shot_n= n_times * 2)
        self._gif_arr[0].save(f'{gif_name}.gif', format='GIF',
                              append_images=self._gif_arr[1:], save_all=True, duration=gif_speed, loop=0)
        
    def __spread(self):
        new_s = self.__get_clear_s()
        for i in range(self.n):
            for j in range(self.m):
                if self.s[i][j][0]: # up
                    if j < self.m - 1:
                        new_s[i][j + 1][0] = self.s[i][j][0]
                    else:
                        new_s[i][0][0] = self.s[i][j][0]
                if self.s[i][j][1]: # right
                    if i < self.n - 1:
                        new_s[i + 1][j][1] = self.s[i][j][1]
                    else:
                        new_s[0][j][1] = self.s[i][j][1]
                if self.s[i][j][2]: # down
                    if j > 0:
                        new_s[i][j - 1][2] = self.s[i][j][2]
                    else:
                        new_s[i][self.m - 1][2] = self.s[i][j][2]
                if self.s[i][j][3]: #left
                    if i > 0:
                        new_s[i - 1][j][3] = self.s[i][j][3]
                    else:
                        new_s[self.n - 1][j][3] = self.s[i][j][3]
        self.s = new_s
                    
    def __collision(self):
        for i in range(self.n):
            for j in range(self.m):
                # https://core.ac.uk/download/pdf/11747817.pdf
                if self.s[i][j] == [1, 0, 1, 0]:
                    self.s[i][j] = [0, 1, 0, 1]
                elif self.s[i][j] == [0, 1, 0, 1]:
                    self.s[i][j] = [1, 0, 1, 0]
                    
    def __draw(self, before_spread, make_gif, gif_name, shot_n):
        for i in range(self.n):
            for j in range(self.m):
                self.ceil_drawer.draw(i, j, self.s[i][j], before_spread=before_spread)
        plt.scatter(x=[-1, -1, self.n + 1, self.n + 1], y=[-1, self.m + 1, -1, self.m + 1], color='white')
        plt.axis('off')
        plt.plot([0, 0, self.n, self.n, 0], [0, self.m, self.m, 0, 0], linestyle='--', color='black')
        if make_gif:
            plot_name = f'{gif_name}_{shot_n}.png'
            plt.savefig(plot_name)
            self._gif_arr.append(Image.open(plot_name))
            os.remove(plot_name)
        plt.show()
        
        if True:
            plot_name = f'{gif_name}_hist_{shot_n}.png'
            plt.bar(range(self.n), np.array(sys.s).sum(axis=-1).sum(axis=-1))
            plt.savefig(plot_name)
            self._gif2_arr.append(Image.open(plot_name))
            os.remove(plot_name)
        
    def __init_random(self, random_type, p, p2=None):
        if random_type == 'uniform':
            for ijk in np.random.permutation(4 * self.n * self.m)[:p]:
                i = int(ijk / 4) % self.n 
                j = int(ijk / (4 * self.n)) 
                k = ijk % 4
                self.s[i][j][k] = 1
        if random_type == '2-uniform':
            for ijk in np.random.permutation(4 * self.n * self.m)[:p2]:
                i = int(ijk / 4) % self.n 
                j = int(ijk / (4 * self.n)) 
                k = ijk % 4
                self.s[i][j][k] = 1
                
    
    def __get_clear_s(self):
        return [[[0, 0, 0, 0] for _ in range(self.n)] for _ in range(self.m)]
    
    
class CeilDrawer:
    
    def __init__(self):
        self.arrow_params = {
            'head_width': 0.2,
            'head_length': 0.2,
        }
        
    def draw(self, i, j, st, before_spread):
        center_x = i + 0.5
        center_y = j + 0.5
        if not before_spread:
            if st[0]:
                self.draw_up_ar(i + 0.5, j)
            if st[1]:
                self.draw_right_ar(i, j + 0.5)
            if st[2]:
                self.draw_down_ar(i + 0.5, j + 1)
            if st[3]:
                self.draw_left_ar(i + 1, j + 0.5)
        else:
            # все стрелки рисуются из центра
            if st[0]:
                self.draw_up_ar(i + 0.5, j + 0.5)
            if st[1]:
                self.draw_right_ar(i + 0.5, j + 0.5)
            if st[2]:
                self.draw_down_ar(i + 0.5, j + 0.5)
            if st[3]:
                self.draw_left_ar(i + 0.5, j + 0.5)
            
    def draw_up_ar(self, x, y):
        plt.arrow(x, y, 0, 0.3, color='blue', **self.arrow_params)
    
    def draw_right_ar(self, x, y):
        plt.arrow(x, y, 0.3, 0, color='yellow', **self.arrow_params)
        
    def draw_down_ar(self, x, y):
        plt.arrow(x, y, 0, -0.3, color='red', **self.arrow_params)
        
    def draw_left_ar(self, x, y):
        plt.arrow(x, y, -0.3, 0, color='green', **self.arrow_params)
        
System(n = 100, m = 100, random_type='uniform', p=100).run(n_times=25, make_gif=True, gif_name='random_uniform', gif_speed=150)