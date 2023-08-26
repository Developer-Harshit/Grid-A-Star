# Basic Screen

import pygame
import sys
from scripts.const import WIDTH, HEIGHT, BG_COLOR, RENDER_SCALE
from scripts.nodemap import NodeMap


print("Starting Game")
NODE_TYPES = ["wall", "ground"]


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Basic Screen")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # display is half of screen size
        self.display = pygame.Surface((WIDTH / RENDER_SCALE, HEIGHT / RENDER_SCALE))

        self.clock = pygame.time.Clock()

        self.file_name = "maps/0.json"
        row = 10 * 2
        col = 10 * 2
        size = 16

        self.node_map = NodeMap(
            (WIDTH / 2 / RENDER_SCALE, HEIGHT / 2 / RENDER_SCALE), size, row, col
        )

        self.current_node = 0

        self.highlight = True
        self.shift_click = False

    def run(self):
        running = True
        while running:
            # For Background ------------------------------------------------------|
            self.display.fill(BG_COLOR)
            # For maze ------------------------------------------------------------|

            self.node_map.draw(self.display)
            mouse_pos = (
                pygame.mouse.get_pos()[0] / RENDER_SCALE,
                pygame.mouse.get_pos()[1] / RENDER_SCALE,
            )

            if self.shift_click:
                self.node_map.change_node(
                    g_pos=mouse_pos, n_type=NODE_TYPES[self.current_node]
                )

            if self.highlight:
                self.node_map.highlight(self.display, mouse_pos)

            # Checking Events -----------------------------------------------------|
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    pass

                    if event.key == pygame.K_i:
                        self.highlight = not self.highlight
                    if event.key == pygame.K_j:
                        self.current_node = 0
                    if event.key == pygame.K_l:
                        self.current_node = 1
                    if event.key == pygame.K_LSHIFT:
                        self.shift_click = True

                    if event.key == pygame.K_k:
                        self.node_map.save(self.file_name)
                    # if event.key == pygame.K_w:
                    #     self.nodemap._moveActive((0, -1))
                    # if event.key == pygame.K_a:
                    #     self.nodemap._moveActive((-1, 0))
                    # if event.key == pygame.K_s:
                    #     self.nodemap._moveActive((0, 1))
                    # if event.key == pygame.K_d:
                    #     self.nodemap._moveActive((1, 0))

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LSHIFT:
                        self.shift_click = False
                    pass
            # Rendering Screen ----------------------------------------------------|
            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Game().run()
    # Quit --------------------------------------------------------------------|
    print("Game Over")
    pygame.quit()
    sys.exit()
    exit()
