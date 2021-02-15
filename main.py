from simulation import Environment, RuleSet, Particle, BoundaryType
from render import get_window, render, main_loop
import time


import numpy as np


env = Environment((40, 40), boundary=BoundaryType.FIXED)

rule = RuleSet(4)
rule.randomize()
# rule.make_symmetric()
print(rule)

env.set_rule(rule)
for _ in range(30):
    env.add_random_particle()
env.give_random_speeds(0, 10)

win = get_window(env)

main_loop(win, env)


