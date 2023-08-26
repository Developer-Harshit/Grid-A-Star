from scripts.utils import draw_square, draw_border, load_image, list_to_location
import json

NEIGHBOR_OFFSET = {"top": (0, -1), "left": (-1, 0), "bottom": (0, 1), "right": (1, 0)}
from random import choice


# works locally and individually
class Node:
    def __init__(self, location, n_type="ground"):
        self.walls = [True, True, True, True]  # top ,left ,bottom ,right

        self.location = location
        self.type = n_type
        self.neighbours = {"top": False, "left": False, "bottom": False, "right": False}

    def get_neighbours(self, nodemap):
        for direction in NEIGHBOR_OFFSET:
            neighbour_loc = (
                str(self.location[0] + NEIGHBOR_OFFSET[direction][0])
                + ";"
                + str(self.location[1] + NEIGHBOR_OFFSET[direction][1])
            )
            if neighbour_loc in nodemap:
                self.neighbours[direction] = nodemap[neighbour_loc]


# works locally
class NodeMap:
    def __init__(self, x_count=0, y_count=0):
        self.map = {}
        self.x_count = x_count
        self.y_count = y_count
        for j in range(y_count):
            for i in range(x_count):
                self.map[list_to_location((i, j))] = Node((i, j))

        self.active_node = [0, 0]

    def save(self, m_path):
        my_map = {}
        for loc in self.map:
            node = self.map[loc]
            my_map[loc] = {"pos": node.location, "type": node.type}

        f = open(m_path, "w")
        json.dump(
            {"map": my_map, "row": self.x_count, "col": self.y_count},
            f,
        )
        f.close()

    def load(self, m_path):
        f = open(m_path, "r")
        map_data = json.load(f)
        f.close()
        self.map = {}
        for loc in map_data["map"]:
            self.map[loc] = Node(
                map_data["map"][loc]["pos"], map_data["map"][loc]["type"]
            )
            pass

        self.x_count = map_data["row"]
        self.y_count = map_data["col"]
        return map_data["size"]

        pass

    def _moveActive(self, direction=(0, 0)):
        if direction[0] == 0 and direction[1] == 0:
            return

        new_node = [
            self.active_node[0] + direction[0],
            self.active_node[1] + direction[1],
        ]
        if list_to_location(new_node) in self.map:
            self.map[list_to_location(self.active_node)].type = "wall"
            self.active_node = new_node

            self.map[list_to_location(self.active_node)].type = "wall"


# works globally

import pygame


class Maze:
    def __init__(self, pos, node_map, size):
        # centre position
        self.pos = pos
        # offset
        self.offset = (
            int(pos[0] - node_map.x_count * size / 2),
            int(pos[1] - node_map.y_count * size / 2),
        )
        # node map object
        self.map = node_map
        for node in self.map.map.values():
            node.get_neighbours(self.map.map)

        # size of each cell
        self.size = size

        self.rect = draw_square(
            size,
        )

        self.assets = {
            "ground": load_image("ground.png", (size, size)),
            "wall": load_image("wall.png", (size, size)),
            "highlight": load_image("highlight.png", (size, size), 200),
        }

        self.border = draw_border(size, (21, 21, 21))

    def extract(self, g_pos):
        for loc in self.map.map:
            node = self.map.map[loc]
            node_pos = self.get_global_pos(node.location)
            node_rect = pygame.Rect(node_pos[0], node_pos[1], self.size, self.size)
            if node_rect.collidepoint(g_pos[0], g_pos[1]):
                return node
        return False

    def change_node(self, g_pos, n_type):
        myNode = self.extract(g_pos)
        if myNode:
            myNode.type = n_type
        pass

    def highlight(self, surf, g_pos):
        node = self.extract(g_pos)

        if node:
            render_pos = self.get_global_pos(node.location)
            surf.blit(self.assets["highlight"], render_pos)

    def get_global_pos(self, local_pos):
        """
        Takes local index/position as arguement and returns global position
        """
        return [
            self.offset[0] + local_pos[0] * (self.size),
            self.offset[1] + local_pos[1] * (self.size),
        ]

    def draw(self, surf):
        for node in self.map.map.values():
            render_pos = self.get_global_pos(node.location)

            surf.blit(self.assets[node.type], render_pos)

            # surf.blit(self.border, render_pos)
