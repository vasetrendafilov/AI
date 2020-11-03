import networkx as nx 
import matplotlib.pyplot as plt 
from collections import deque

class Graph(object):

    def __init__(self, graph={}):
        self.graph = graph
        self.visual = [] 

    def vertices(self):
        return list(self.graph.keys())

    def edges(self):
        edges = []
        for vertex in self.graph:
            for neighbour in self.graph[vertex]:
                edges.append((vertex, neighbour))
        return edges

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, edge, reverse=True):
        vertex1, vertex2 = edge
        self.graph[vertex1].append(vertex2)
        self.visual.append([vertex1, vertex2])
        if reverse:
            self.graph[vertex2].append(vertex1)
            self.visual.append([vertex2, vertex1])

    def remove_vertex(self, vertex_to_remove):
        if vertex_to_remove in self.graph:
            del self.graph[vertex_to_remove]
            for vertex in self.vertices():
                if vertex_to_remove in self.graph[vertex]:
                    self.graph[vertex].remove(vertex_to_remove)

    def remove_edge(self, edge, reverse=True):
        vertex1, vertex2 = edge
        if vertex2 in self.graph[vertex1]:
            self.graph[vertex1].remove(vertex2)
        if reverse and vertex1 not in self.graph[vertex2]:
            self.graph[vertex2].append(vertex1)

    def search(self, algo, starting_vertex, goal_vertex, verbose=False):

        if starting_vertex == goal_vertex:
            if verbose:
                print('Почетниот и бараниот јазол се исти')
            return []

        visited = {starting_vertex}
        queue = deque([[starting_vertex]])

        while queue:
            if verbose:
                print('Ред за разгранување:')
                for element in queue:
                    print(element, end=' ')
                print()
                print()

            vertex_list = queue.popleft()
            vertex_to_expand = vertex_list[-1]
            if verbose:
                print('Го разгрануваме јазолот {}'.format(vertex_to_expand))
            for neighbour in self.graph[vertex_to_expand]:
                if neighbour in visited:
                    if verbose:
                        print('{} е веќе посетен'.format(neighbour))
                else:
                    if verbose:
                        print('{}, кој е соседен јазол на {} го немаме посетено до сега, затоа го додаваме во редот '
                              'за разгранување и го означуваме како посетен'.format(neighbour, vertex_to_expand))
                    if neighbour == goal_vertex:
                        if verbose:
                            print('Го пронајдовме посакуваниот јазол {}. Патеката да стигнеме до тука е {}'
                                  .format(neighbour, vertex_list + [neighbour]))
                        return vertex_list + [neighbour]
                    visited.add(neighbour)
                    if algo == "bfs":
                        queue.append(vertex_list + [neighbour])
                    elif algo == "dfs":
                        queue.appendleft(vertex_list + [neighbour])
            if verbose:
                print()

    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.visual)
        nx.draw_networkx(G)
        plt.show()

    def __str__(self):
        return f'Vertices: {self.vertices()}\n Edges: {self.edges()}'