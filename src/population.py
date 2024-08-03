import config
import player
import math
import species
import operator

class Population:
    def __init__(self, size = 256) -> None:
        self.players = []
        self.generation = 0
        self.species = []
        self.size = size

        for _ in range(self.size):
            self.players.append(player.Player())


    def update_live_players(self):
        number_alive = 0

        for player in self.players:
            if player.alive:
                player.ai_look(config.ground.y)
                player.ai_think()
                player.draw(config.window)
                player.update(config.ground.rectangle)

                number_alive += 1

        return number_alive


    def extinct(self):
        for player in self.players:
            if player.alive:
                return False

        return True
    

    def speciate(self):
        for s in self.species:
            s.players = []

        for player in self.players:
            add = False

            for s in self.species:
                if s.similarity(player.brain):
                    s.add(player)
                    add = True
                    break

            if not add:
                self.species.append(species.Species(player))


    def fitness(self):
        for player in self.players:
            player.ai_calculate_fitness()

        for s in self.species:
            s.calculate_fitness()


    def sort_fitness(self):
        for s in self.species:
            s.sort_fitness()

        self.species.sort(key=operator.attrgetter('benchmark_fitness'), reverse=True)


    def next_generation(self):
        children = []

        # survival of the fitest
        for s in self.species:
            children.append(s.champion.clone())

        # fill open slots with children
        children_per_species = math.floor((self.size - len(self.species)) / len(self.species))

        for s in self.species:
            for _ in range(children_per_species):
                children.append(s.offspring())

        while len(children) < self.size:
            children.append(self.species[0].offspring())

        self.players = children
        self.generation += 1


    def kill_extinct_species(self):
        for s in self.species:
            if len(s.players) == 0:
                self.species.remove(s)


    def kill_stale_species(self):
        species_bin = []
        for s in self.species:
            if s.staleness >= 8:
                if len(self.species) > len(species_bin) + 1:
                    species_bin.append(s)

                    for player in s.players:
                        self.players.remove(player)
                else:
                    s.staleness = 0

        for species in species_bin:
            self.species.remove(species)


    def natural_selection(self):
        self.speciate()
        self.fitness()
        self.kill_extinct_species()
        self.kill_stale_species()
        self.sort_fitness()
        self.next_generation()
