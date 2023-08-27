from random import random, randint, choice
from scripts.utils import load_image


class Agent:
    def __init__(self, nodemap, goal=False):
        self.nodemap = nodemap
        self.goal = goal
        avl_node = []
        for node in nodemap.map.values():
            if node.type == "ground":
                avl_node.append(node)
        self.start = choice(avl_node)
        self.assets = {
            "start": load_image("agent/start.png", (nodemap.size, nodemap.size)),
            "end": load_image("agent/end.png", (nodemap.size, nodemap.size)),
            "open": load_image("agent/open.png", (nodemap.size, nodemap.size)),
            "close": load_image("agent/close.png", (nodemap.size, nodemap.size)),
            "path": load_image("agent/path.png", (nodemap.size, nodemap.size)),
        }
        if not goal:
            self.goal = choice(avl_node)
        self.openset = [self.start]
        self.start.g = 0
        self.closeset = []

        self.cameFrom = {}

    def reconstruct(self, current):
        path = [current]

        while current.str_location() in self.cameFrom:
            current = self.cameFrom[current.str_location()]
            path.insert(0, current)

        return path

        pass

    def get_current(self):
        current = False
        for node in self.openset:
            node.heuristics(self.goal)
            if current:
                if current.f > node.f:
                    current = node
            else:
                current = node
        return current

    def a_star(self):
        if len(self.openset) == 0:
            prnt("No Solution")
        else:
            current = self.get_current()
            if current == self.goal:
                return self.reconstruct(current)
            self.openset.remove(current)
            self.closeset.append(current)

            for neighbor in current.get_neighbours(self.nodemap.map):
                if not neighbor:
                    continue
                if neighbor.type == "wall":
                    continue
                tentG = current.g + 1

                if tentG < neighbor.g:
                    self.cameFrom[neighbor.str_location()] = current
                    neighbor.g = tentG
                    neighbor.f = tentG + neighbor.heuristics(self.goal)
                if neighbor not in self.openset:
                    if neighbor not in self.closeset:
                        self.openset.append(neighbor)

    def move_random(self):
        neighbours = self.start.get_neighbours(self.nodemap.map)
        avl_node = []
        for node in neighbours:
            if node:
                if node.type == "ground":
                    avl_node.append(node)
        self.start = choice(avl_node)

    def draw(self, surf):
        for node in self.closeset:
            surf.blit(self.assets["open"], self.nodemap.get_global_pos(node.location))
        for node in self.reconstruct(self.get_current()):
            surf.blit(self.assets["path"], self.nodemap.get_global_pos(node.location))

        surf.blit(
            self.assets["start"], self.nodemap.get_global_pos(self.start.location)
        )
        surf.blit(self.assets["end"], self.nodemap.get_global_pos(self.goal.location))
