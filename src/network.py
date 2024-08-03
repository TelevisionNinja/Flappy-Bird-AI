import node
import connection
import random

class Network:
    def __init__(self, inputs, clone = False) -> None:
        self.connections = []
        self.nodes = []
        self.inputs = inputs
        self.network = []
        self.layers = 2

        if clone:
            return

        for i in range(self.inputs):
            self.nodes.append(node.Node(i))
            self.nodes[i].layer = 0

        # bias
        self.nodes.append(node.Node(self.layers + 1))
        self.nodes[self.layers + 1].layer = 0
        
        # output
        self.nodes.append(node.Node(self.layers + 2))
        self.nodes[self.layers + 2].layer = 1

        # connections
        for i in range(self.layers + 2):
            self.connections.append(connection.Connection(self.nodes[i], self.nodes[self.layers + 2], random.uniform(-1, 1)))


    def connect_nodes(self):
        for i in range(len(self.nodes)):
            self.nodes[i].connections = []

        for i in range(len(self.connections)):
            self.connections[i].from_node.connections.append(self.connections[i])


    def generate_network(self):
        self.connect_nodes()
        self.network = []

        for l in range(self.layers):
            for n in range(len(self.nodes)):
                if self.nodes[n].layer == l:
                    self.network.append(self.nodes[n])


    def feed_forward(self, vision):
        for i in range(self.inputs):
            self.nodes[i].output = vision[i]

        self.nodes[self.layers + 1].output = 1

        for i in range(len(self.network)):
            self.network[i].activate()
        
        output = self.nodes[self.layers + 2].output

        for i in range(len(self.nodes)):
            self.nodes[i].input = 0

        return output


    def clone(self):
        clone = Network(self.inputs, True)

        for node in self.nodes:
            clone.nodes.append(node.clone())
        
        for connection in self.connections:
            clone.connections.append(connection.clone(clone.get_node(connection.from_node.id),
                                                      clone.get_node(connection.to_node.id)))
        
        clone.layers = self.layers
        clone.connect_nodes()
        return clone


    def get_node(self, id):
        for node in self.nodes:
            if node.id == id:
                return node


    def mutate(self):
        if random.uniform(0, 1) < 0.8:
            for connection in self.connections:
                connection.mutate_weight()
