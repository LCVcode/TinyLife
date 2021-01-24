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


def main_loop(window, env):
    clock = pg.time.Clock()

    running, paused = True, False

    while running:
        time = clock.tick(60) #similar to timerDelay

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        if not paused:
            env.tick(0.05)
            render(window, env)

    pygame.quit()

