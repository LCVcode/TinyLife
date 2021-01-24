from simulation import Particle, Environment
import pygame as pg


_config = {
        'scale': 10,
        'colors': [(178, 34, 34),  # Firebrick
                   ( 30,144,255),  # Dodger blue
                   (255,215,  0),  # Gold
                   (255,  0,255),  # Magenta
                   ],
        'bg':( 40, 40, 40)
        }


def get_window(env):
    if not isinstance(env, Environment):
        raise TypeError(f"Expected Environment, got {type(env)}")

    shape = map(lambda x: x*_config['scale'], env.shape)
    window = pg.display.set_mode(tuple(shape))

    return window

def render(window, env):
    window.fill(_config['bg'])
    scale = _config['scale']

    for par in env._particles:
        pos = (par.pos[0][0] * scale + (env.width * scale / 2),
               par.pos[0][1] * scale + (env.height * scale / 2))
        color = _config['colors'][par.id]

        pg.draw.circle(window, color, pos, scale)

    pg.display.flip()

