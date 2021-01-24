from simulation import Environment, RuleSet, Particle, BoundaryType
from render import get_window, render, main_loop
import time


import numpy as np


env = Environment((40, 80), boundary=BoundaryType.TORUS)

rule = RuleSet(4)
rule.randomize()
rule.make_symmetric()

env.set_rule(rule)
for _ in range(25):
    env.add_random_particle()

win = get_window(env)

main_loop(win, env)


