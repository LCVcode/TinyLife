from simulation import Environment, RuleSet, Particle, BoundaryType
from render import get_window, render, main_loop
import time


import numpy as np


env = Environment((20, 20), boundary=BoundaryType.FIXED)

rule = RuleSet(4)
rule.randomize()
rule.make_symmetric()

rule._forces[0].x1 = 2
rule._forces[0].x2 = 3
rule._forces[0].x3 = 4
rule._forces[0].c = 5
rule._forces[0].a = 10

print(rule)

env.set_rule(rule)
for _ in range(30):
    env.add_random_particle()
env.give_random_speeds(0, 10)

win = get_window(env)

main_loop(win, env)


