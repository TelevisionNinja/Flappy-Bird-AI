import operator
import random

class Species:
    def __init__(self, player) -> None:
        self.players = []
        self.fitness = 0
        self.threshold = 1.2
        self.players.append(player)
        self.benchmark_fitness = player.fitness
        self.benchmark_brain = player.brain.clone()
        self.champion = player.clone()
        self.staleness = 0


    def similarity(self, brain):
        similarity = Species.weight_difference(self.benchmark_brain, brain)
        return self.threshold > similarity


    def weight_difference(benchmark_brain, brain):
        total_difference = 0

        for i in range(len(benchmark_brain.connections)):
            for j in range(len(brain.connections)):
                if i == j:
                    total_difference += abs(benchmark_brain.connections[i].weight - brain.connections[i].weight)

        return total_difference


    def add(self, player):
        self.players.append(player)


    def sort_fitness(self):
        self.players.sort(key=operator.attrgetter('fitness'), reverse=True)

        if self.players[0].fitness > self.benchmark_fitness:
            self.staleness = 0
            self.benchmark_fitness = self.players[0].fitness
            self.champion = self.players[0].clone()
        else:
            self.staleness += 1


    def calculate_fitness(self):
        total_fitness = 0

        for player in self.players:
            total_fitness += player.fitness

        if len(self.players) > 0:
            self.fitness = total_fitness // len(self.players)
        else:
            self.fitness = 0


    def offspring(self):
        length = len(self.players)
        baby = None

        if length > 1:
            baby = self.players[random.randint(1, length - 1)].clone() # not index 0 so that we dont clone the champion
        else:
            baby = self.players[0].clone()

        baby.brain.mutate()
        return baby
