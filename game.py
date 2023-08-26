# Basic Screen

import pygame
import sys
from scripts.const import WIDTH, HEIGHT, BG_COLOR, RENDER_SCALE
from scripts.node import Maze, NodeMap


print("Starting Game")


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Basic Screen")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # display is half of screen size
        self.display = pygame.Surface((WIDTH / RENDER_SCALE, HEIGHT / RENDER_SCALE))

        self.clock = pygame.time.Clock()

        self.nodemap = NodeMap()

        self.maze = Maze(
            (WIDTH / 2 / RENDER_SCALE, HEIGHT / 2 / RENDER_SCALE),
            self.nodemap,
            self.nodemap.load("maps/69.json"),
        )

    def run(self):
        running = True
        while running:
            # For Background ------------------------------------------------------|
            self.display.fill(BG_COLOR)

            self.maze.draw(self.display)

            # Checking Events -----------------------------------------------------|
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    pass

                if event.type == pygame.KEYUP:
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
