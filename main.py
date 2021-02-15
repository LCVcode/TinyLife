from simulation import Environment, RuleSet, Particle, BoundaryType
from render import get_window, render, main_loop
import time


import numpy as np


env = Environment((20, 20), boundary=BoundaryType.TORUS)

rule = RuleSet(2)
rule.randomize()

rule._forces[0].x1 = 3
rule._forces[0].x2 = 6
rule._forces[0].x3 = 15
rule._forces[0].c = 20
rule._forces[0].a = -18

rule._forces[2].x1 = 2
rule._forces[2].x2 = 5
rule._forces[2].x3 = 20
rule._forces[2].c = 4
rule._forces[2].a = 17.5

rule._forces[3].x1 = 2
rule._forces[3].x2 = 4
rule._forces[3].x3 = 6
rule._forces[3].c = 20
rule._forces[3].a = -2.5

rule.make_symmetric()

print(rule)

env.set_rule(rule)
for _ in range(20):
    env.add_random_particle()
env.give_random_speeds(0, 1)

win = get_window(env)

main_loop(win, env)


