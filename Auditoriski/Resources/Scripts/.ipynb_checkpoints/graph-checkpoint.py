import heapq
import networkx as nx 
import matplotlib.pyplot as plt 
from collections import deque

class Graph(object):

    def __init__(self, graph={}):
        self.graph = graph

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
        if reverse:
            self.graph[vertex2].append(vertex1)

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

    def search_find_path(self, algo, starting_vertex, goal_vertex, verbose=False):

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

    def search_traversal(self, algo, starting_vertex, goal_vertex):
        visited = {starting_vertex}
        states_queue = deque([starting_vertex])
        while states_queue:
            state_to_expand = states_queue.popleft()
            for next_state in  self.graph[state_to_expand]:
                if next_state not in visited:
                    if next_state == goal_vertex:
                        return next_state
                    visited.add(next_state)
                    if algo == 'dfs':
                        states_queue.appendleft(next_state)
                    elif algo == 'bfs':
                        states_queue.append(next_state)
        return
    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.edges())
        nx.draw_networkx(G)
        plt.show()

    def __str__(self):
        return f'Vertices: {self.vertices()}\n Edges: {self.edges()}'



class WeightedGraph(object):
    def __init__(self,graph={}):
        self.graph = graph

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = {}

    def vertices(self):
        return list(self.graph.keys())

    def add_edge(self, edge, add_reversed=True):
        vertex1, vertex2, weight = edge
        self.graph[vertex1][vertex2] = weight
        if add_reversed:
            self.graph[vertex2][vertex1] = weight

    def edges(self, visual=False):
        edges = []
        for vertex in self.graph:
            for neighbour, weight in self.graph[vertex].items():
                if visual:
                    edges.append((vertex, neighbour))
                else:
                    edges.append((vertex, neighbour, weight))
        return edges

    def neighbours(self, vertex):
        return list(self.graph[vertex].items())

    def uniform_cost_search(self, starting_vertex, goal_vertex, verbose=False):
        if starting_vertex == goal_vertex:
            if verbose:
                print('Почетниот и бараниот јазол се исти')
            return
        expanded = set()
        queue = [(0, [starting_vertex])]
        heapq.heapify(queue)
        while queue:
            if verbose:
                print('Ред за разгранување:')
                for element in queue:
                    print(element, end=' ')
                print()
                print()
            weight, vertex_list = heapq.heappop(queue)
            vertex_to_expand = vertex_list[-1]
            if vertex_to_expand == goal_vertex:
                if verbose:
                    print('Го пронајдовме посакуваниот јазол {}. Патеката да стигнеме до тука е {} со цена {}'
                          .format(vertex_to_expand, vertex_list, weight))
                return weight, vertex_list
            if vertex_to_expand in expanded:
                if verbose:
                    print('{} е веќе разгранет'.format(vertex_to_expand, weight, vertex_list))
                continue
            if verbose:
                print('Го разгрануваме јазолот {} од ({}, {})'.format(vertex_to_expand, weight, vertex_list))
            for neighbour, new_weight in self.neighbours(vertex_to_expand):
                if neighbour in expanded:
                    if verbose:
                        print('{} е веќе разгранет'.format(neighbour))
                else:
                    if verbose:
                        print('{} со тежина {}, кој е соседен јазол на {}, го додаваме во редот за разгранување со нова '
                              'цена и го означуваме како разгранет'.format(neighbour, new_weight, vertex_to_expand))
                    heapq.heappush(queue, (weight + new_weight, vertex_list + [neighbour]))
            expanded.add(vertex_to_expand)
            if verbose:
                print()

    def visualize(self):
        G = nx.Graph()
        G.add_edges_from(self.edges(True))
        nx.draw_networkx(G)
        plt.show()

    def __str__(self):
        return f'Vertices: {self.vertices()}\n Edges: {self.edges()}'    