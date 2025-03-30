class Hypergraph:
    def __init__(self, filename):
        self.num_edges = None
        self.num_vertices = None
        self.vertices = set()
        self.edges = []
        self.read_hypergraph(filename)

    def read_hypergraph(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith('c'):
                    continue  # Ignore comments
                if line.startswith('p'):
                    parts = line.split()
                    self.num_vertices = int(parts[2])
                    self.num_edges = int(parts[3])
                else:
                    edge = set(map(int, line.split()))
                    self.edges.append(edge)
                    self.vertices.update(edge)

    def __repr__(self):
        return f"Hypergraph(vertices={self.vertices}, edges={self.edges})"
