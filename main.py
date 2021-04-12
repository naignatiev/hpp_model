from model import HPP
from base import State, RandomInit

# task 1
task_1 = False
if task_1:
    state = State(100, 100)
    RandomInit.uniform(state, 100)
    model = HPP(state, 'test', 'test_hist', gif_speed=300)
    model.run(100)

# task 2
task_2 = False
if task_2:
    state = State(200, 200)
    RandomInit.uniform_2(state, p1=400, p2=500)
    model = HPP(state, 'task2', 'task2_hist', gif_speed=100)
    model.run(100)

# task 3
task_3 = True
if task_3:
    state = State(200, 200)
    RandomInit.circle(state, 100, 100, r=20, p_sphere=500, p_env=400)
    model = HPP(state, 'task3', 'task3_hist', gif_speed=100)
    model.run(100)
