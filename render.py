from simulation import Particle, Environment
import pygame as pg

pg.init()

_font = pg.font.SysFont(None, 16)
_config = {
        'scale': 10,
        'colors': [(178, 34, 34),  # Firebrick
                   ( 30,144,255),  # Dodger blue
                   (255,215,  0),  # Gold
                   (255,  0,255),  # Magenta
                   (  0,255,  0),  # Lime
                   (244,164, 96),  # Sandy brown
                   (176,196,222),  # Light steel blue
                   ],
        'bg':( 40, 40, 40)
        }


def get_window(env):
    if not isinstance(env, Environment):
        raise TypeError(f"Expected Environment, got {type(env)}")

    shape = map(lambda x: x*_config['scale'], env.shape)
    window = pg.display.set_mode(tuple(shape))

    return window


def render(window, env, fps):
    window.fill(_config['bg'])
    scale = _config['scale']

    for par in env._particles:
        pos = (par.pos[0][0] * scale + (env.width * scale / 2),
               par.pos[0][1] * scale + (env.height * scale / 2))
        color = _config['colors'][par.id]

        try:
            pg.draw.circle(window, color, pos, scale)
        except TypeError as e:
            print(pos)
            print(e)

    metrics = _font.render(str(fps), True, (255,255,255))
    window.blit(metrics, (5, 5))

    pg.display.flip()


def main_loop(window, env):
    clock = pg.time.Clock()

    running, paused = True, False

    while running:
        clock.tick(60)
        fps = int(clock.get_fps())

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

                if event.key == pg.K_SPACE:
                    paused = not paused

        if not paused:
            env.tick(0.05)
            render(window, env, fps)

    pg.quit()

