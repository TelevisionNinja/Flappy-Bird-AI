import random


def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))


class Connection:
    def __init__(self, from_node, to_node, weight) -> None:
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight


    def mutate_weight(self):
        if random.uniform(0, 1) < 0.1:
            self.weight = random.uniform(-1, 1)
        else:
            self.weight += random.gauss(0, 1) / 10
            self.weight = clamp(self.weight, -1, 1)


    def clone(self, from_node, to_node):
        return Connection(from_node, to_node, self.weight)
