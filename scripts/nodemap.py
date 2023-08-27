from random import choice
from scripts.utils import draw_square, draw_border, load_image, list_to_location
import json

import pygame

NEIGHBOR_OFFSET = {"top": (0, -1), "left": (-1, 0), "bottom": (0, 1), "right": (1, 0)}


# works locally and individually
class Node:
    def __init__(self, location, n_type="ground"):
        self.walls = [True, True, True, True]  # top ,left ,bottom ,right

        self.location = location
        self.type = n_type

        self.g = 10**10
        self.h = 0
        self.f = 0

    def str_location(self):
        return list_to_location(self.location)

    def gCost(self, other):
        self.g = other.g + 1
        return self.g

    def heuristics(self, goal):
        self.h = abs(self.location[0] - goal.location[0]) + abs(
            self.location[1] - goal.location[1]
        )
        return self.h

    def get_neighbours(self, nodemap):
        result = []
        for direction in NEIGHBOR_OFFSET:
            neighbour_loc = (
                str(self.location[0] + NEIGHBOR_OFFSET[direction][0])
                + ";"
                + str(self.location[1] + NEIGHBOR_OFFSET[direction][1])
            )
            if neighbour_loc in nodemap:
                result.append(nodemap[neighbour_loc])
        return result


#     def _moveActive(self, direction=(0, 0)):
#         if direction[0] == 0 and direction[1] == 0:
#             return

#         new_node = [
#             self.active_node[0] + direction[0],
#             self.active_node[1] + direction[1],
#         ]
#         if list_to_location(new_node) in self.map:
#             self.map[list_to_location(self.active_node)].type = "wall"
#             self.active_node = new_node

#             self.map[list_to_location(self.active_node)].type = "wall"


# works globally


class NodeMap:
    def __init__(self, pos, size=16, row=0, col=0):
        self.pos = pos
        self.size = size
        self.row = row
        self.col = col

        # Getting Offset
        self.update_offset()

        # Assets
        self.assets = {
            "ground": load_image("ground.png", (size, size)),
            "wall": load_image("wall.png", (size, size)),
            "highlight": load_image("highlight.png", (size, size), 200),
        }

        # Optional to do -------------------------------------------
        self.map = {}
        for j in range(col):
            for i in range(row):
                self.map[list_to_location((i, j))] = Node((i, j))
        # ---------------------------------------------------------

    def draw(self, surf):
        for loc in self.map:
            node = self.map[loc]
            render_pos = self.get_global_pos(node.location)
            surf.blit(self.assets[node.type], render_pos)

    def extract(self, g_pos):
        for loc in self.map:
            node = self.map[loc]
            pos = self.get_global_pos(node.location)
            node_rect = pygame.Rect(pos[0], pos[1], self.size, self.size)

            if node_rect.collidepoint(g_pos[0], g_pos[1]):
                return node
        return False

    def get_global_pos(self, local_pos):
        """
        Takes local index/position as arguement and returns global position
        """
        return [
            self.offset[0] + local_pos[0] * (self.size),
            self.offset[1] + local_pos[1] * (self.size),
        ]

    def save(self, m_path):
        my_map = {}
        for loc in self.map:
            node = self.map[loc]
            my_map[loc] = {"pos": node.location, "type": node.type}

        f = open(m_path, "w")
        json.dump(
            {
                "map": my_map,
                "row": self.row,
                "col": self.col,
                "size": self.size,
            },
            f,
        )
        f.close()

    def load(self, m_path):
        map_data = {}
        try:
            f = open(m_path, "r")
            map_data = json.load(f)
            f.close()
        except FileNotFoundError:
            print("File not Found")
            return False
        self.map = {}
        for loc in map_data["map"]:
            self.map[loc] = Node(
                map_data["map"][loc]["pos"], map_data["map"][loc]["type"]
            )
            pass

        self.row = map_data["row"]
        self.col = map_data["col"]
        self.size = map_data["size"]

        self.update_offset()

    def update_offset(self):
        self.offset = (
            int(self.pos[0] - self.row * self.size / 2),
            int(self.pos[1] - self.col * self.size / 2),
        )

    def change_node(self, g_pos, n_type):
        myNode = self.extract(g_pos)
        if myNode:
            myNode.type = n_type

    def highlight(self, surf, g_pos):
        myNode = self.extract(g_pos)

        if myNode:
            render_pos = self.get_global_pos(myNode.location)
            surf.blit(self.assets["highlight"], render_pos)
