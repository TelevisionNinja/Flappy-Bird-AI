import pygame
import random
import config
import network


class Player:
    def __init__(self, x = 128, y = 200) -> None:
        self.x = x
        self.y = y
        self.size = (20, 20) # x, y
        self.rectangle = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.velocity = 0
        self.can_flap = False
        self.alive = True
        self.score = 0
        self.passed_pipe = None

        self.ai_decision = None
        self.vision = [0.5, 0.5, 0.5]
        self.inputs = 3
        self.brain = network.Network(self.inputs)
        self.brain.generate_network()
        self.lifespan = 0
        self.fitness = 0


    def draw(self, window):
        pygame.draw.rect(surface=window, color=self.color, rect=self.rectangle)


    def ground_collision(self, ground):
        return pygame.Rect.colliderect(self.rectangle, ground)


    def sky_collision(self):
        return self.rectangle.y < self.size[1]


    def pipe_collision(self):
        for pipe in config.pipes:
            return pygame.Rect.colliderect(self.rectangle, pipe.top_rectangle) or pygame.Rect.colliderect(self.rectangle, pipe.bottom_rectangle)


    def update(self, ground):
        if not self.ground_collision(ground) and not self.pipe_collision():
            # gravity

            self.velocity += 0.25
            self.velocity = min(self.velocity, 8)

            self.rectangle.y += self.velocity
            self.lifespan += 1

            # score
            passed_pipe = None

            for pipe in config.pipes:
                if pipe.passed:
                    passed_pipe = pipe
                    break

            if passed_pipe is not None and passed_pipe != self.passed_pipe:
                self.score += 1
                self.passed_pipe = passed_pipe
        else:
            self.alive = False
            self.velocity = 0
            self.can_flap = False


    def flap(self):
        if not self.can_flap and not self.sky_collision():
            self.can_flap = True
            self.velocity = -6

        if self.velocity >= 0:
            self.can_flap = False


    def ai_think(self):
        self.ai_decision = self.brain.feed_forward(self.vision)

        threshold = 0.73
        if self.ai_decision > threshold:
            self.flap()


    def closest_pipe():
        for pipe in config.pipes:
            if not pipe.passed:
                return pipe


    def ai_look(self, ground_level):
        if len(config.pipes) != 0:
            closest_pipe = Player.closest_pipe()

            # to top pipe
            self.vision[0] = max(0, self.rectangle.center[1] - closest_pipe.top_rectangle.bottom) / ground_level
            pygame.draw.line(config.window, self.color, self.rectangle.center, (self.rectangle.center[0], closest_pipe.top_rectangle.bottom))

            # to opening center
            self.vision[1] = max(0, closest_pipe.x - self.rectangle.center[0]) / ground_level
            pygame.draw.line(config.window, self.color, self.rectangle.center, (closest_pipe.x, self.rectangle.center[1]))

            # to bottom pipe
            self.vision[2] = max(0, closest_pipe.bottom_rectangle.top - self.rectangle.center[1]) / ground_level
            pygame.draw.line(config.window, self.color, self.rectangle.center, (self.rectangle.center[0], closest_pipe.bottom_rectangle.top))


    def ai_calculate_fitness(self):
        self.fitness = self.lifespan


    def clone(self):
        clone = Player()
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generate_network()
        return clone
