def relu(x):
    return max(0, x)


class Node:
    def __init__(self, id) -> None:
        self.id = id
        self.layer = 0
        self.input = 0
        self.output = 0
        self.connections = []


    def activate(self):
        match self.layer:
            case 1:
                self.output = relu(self.input)

        for i in range(len(self.connections)):
            self.connections[i].to_node.input += self.connections[i].weight * self.output


    def clone(self):
        clone = Node(self.id)
        clone.id = self.id
        clone.layer = self.layer
        return clone
