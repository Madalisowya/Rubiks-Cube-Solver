import numpy as np
import networkx as nx

# Color constants for faces
green = 0
blue = 1
white = 2
yellow = 3
red = 4
orange = 5

# Dictionary to store faces with corresponding color codes
face = {
    white: np.array([
        ["w", "w", "w"],
        ["w", "w", "w"],
        ["w", "w", "w"]
    ]),
    yellow: np.array([
        ["y", "y", "y"],
        ["y", "y", "y"],
        ["y", "y", "y"]
    ]),
    green: np.array([
        ["g", "g", "g"],
        ["g", "g", "g"],
        ["g", "g", "g"]
    ]),
    blue: np.array([
        ["b", "b", "b"],
        ["b", "b", "b"],
        ["b", "b", "b"]
    ]),
    red: np.array([
        ["r", "r", "r"],
        ["r", "r", "r"],
        ["r", "r", "r"]
    ]),
    orange: np.array([
        ["o", "o", "o"],
        ["o", "o", "o"],
        ["o", "o", "o"]
    ])
}

class Surrounding_faces:
    def __init__(self, connections):
        self.connections = connections
        self.graph = self.create_graph()

    def create_graph(self):
        graph = nx.DiGraph()  # Use DiGraph to represent a directed graph

        for node, neighbors in self.connections.items():
            for neighbor, weight in neighbors.items():
                graph.add_edge(node, neighbor, weight=weight)

        return graph

    # Depth-First Search (DFS) function to traverse the graph
    def dfs(self, node, visited):
        # If the current node has not been visited yet
        if not visited[node]:
            # Mark the current node as visited
            visited[node] = True
            # Find neighbors of the current node
            neighbours = np.nonzero(nx.to_numpy_array(self.graph[node]))[0]
            # Recursively apply DFS to unvisited neighbors
            for neighbour in neighbours:
                self.dfs(neighbour, visited)

# connections for each node (each face connected to other faces, number is its weight )
connections = {
    green: {white: 1, red: 2, yellow: 3, orange: 4},
    blue: {white: 1, orange: 2, yellow: 3, red: 4},
    white: {blue: 1, red: 2, green: 3, orange: 4},
    yellow: {green: 1, red: 2, blue: 3, orange: 4},
    red: {white: 1, blue: 2, yellow: 3, green: 4},
    orange: {white: 1, green: 2, yellow: 3, blue: 4}
}

# Instantiate the class
surr = Surrounding_faces(connections)

# Print the adjacency matrix
print("Adjacency Matrix:")
adj_matrix = nx.to_numpy_array(surr.graph, nodelist=sorted(surr.graph.nodes()), weight='weight', dtype=int)

print(adj_matrix)


