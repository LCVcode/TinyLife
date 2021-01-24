from simulation import Environment, RuleSet, Particle
from render import get_window, render
import time


import numpy as np


env = Environment((40, 35))

rule = RuleSet(4)
rule.randomize()
rule.make_symmetric()

env.set_rule(rule)

env.add_particle((0, 0), 1)
env.add_particle((-10, -8), 1)
env.add_particle((4, 3), 0)
env.add_particle((-3, 5), 0)
env.add_particle((-5, 0), 2)
env.add_particle((5, 50), 2)
env.add_particle((-1, -4), 3)
env.add_particle((-20, -20), 3)

win = get_window(env)

while True:
    render(win, env)
    env.tick(0.1)

time.sleep(2)

