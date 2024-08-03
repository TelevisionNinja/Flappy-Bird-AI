import pygame
import config
import components
import population


def generate_pipe():
    config.pipes.append(components.Pipes(config.window_width, config.window_height))


def get_current_best_score(birds):
    best_score = 0

    for player in birds.players:
        if player.alive:
            best_score = max(best_score, player.score)

    return best_score


def main():
    pygame.init()
    clock = pygame.time.Clock()
    pipe_spawn_time = 0
    population_size = 256
    birds = population.Population(population_size)
    font = pygame.font.SysFont(name=None, size=25)
    best_score = 0
    speed_up = False
    number_alive = population_size

    while True:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    return
                case pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()

                    if keys[pygame.K_SPACE]:
                        speed_up = not speed_up

        # background
        config.window.fill(color=(25, 125, 200))

        # ground
        config.ground.draw(config.window)

        # pipes
        if pipe_spawn_time <= 0:
            generate_pipe()
            pipe_spawn_time = 256
        pipe_spawn_time -= 1

        for pipe in config.pipes:
            if pipe.off_screen:
                config.pipes.remove(pipe)
            else:
                pipe.draw(config.window)
                pipe.update()

        # color certain pipes
        for pipe in config.pipes:
            if not pipe.passed:
                pipe.color = (255, 0, 0)
                break
            else:
                pipe.color = (0, 0, 0)

        current_best_score = get_current_best_score(birds)
        best_score = max(best_score, current_best_score)
        best_score_text_surface = font.render(f'Generation: {birds.generation + 1}    Best Score: {best_score}    Current Score: {current_best_score}    Birds Alive: {number_alive}', False, (0, 0, 0))

        # genetic
        if not birds.extinct():
            number_alive = birds.update_live_players()
        else:
            config.pipes.clear()
            birds.natural_selection()

        config.window.blit(best_score_text_surface, (20, config.window_height - 20 - 30))

        pygame.display.flip()

        # frame rate
        if not speed_up:
            clock.tick(60)
        else:
            clock.tick(0)


if __name__ == '__main__':
    main()
