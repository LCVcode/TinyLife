from simulation import Environment, RuleSet, Particle, BoundaryType
from render import get_window, render
import time


import numpy as np


env = Environment((40, 80), boundary=BoundaryType.TORUS)

rule = RuleSet(4)
rule.fill(0)

rule._val[0][1] = 1
rule._val[1][2] = 1
rule._val[2][0] = -0.5
rule._val[0][0] = -0.2
rule._val[1][1] = -0.2

rule.make_symmetric()
rule.randomize()

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

