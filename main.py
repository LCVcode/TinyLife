from simulation import Environment, RuleSet, Particle, BoundaryType
from render import get_window, render, main_loop
import time


import numpy as np


env = Environment((10, 10), boundary=BoundaryType.FIXED)

rule = RuleSet(3)
rule.randomize()
# rule.make_symmetric()
print(rule)

env.set_rule(rule)
for _ in range(15):
    env.add_random_particle()

for particle in env._particles:
    print(particle.pos)

win = get_window(env)

main_loop(win, env)


