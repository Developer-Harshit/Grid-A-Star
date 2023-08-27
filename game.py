# Main

import pygame
import sys
from scripts.const import WIDTH, HEIGHT, BG_COLOR, RENDER_SCALE
from scripts.nodemap import NodeMap
from scripts.agent import Agent


print("Starting Game")


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Main")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # display is half of screen size
        self.display = pygame.Surface((WIDTH / RENDER_SCALE, HEIGHT / RENDER_SCALE))

        self.clock = pygame.time.Clock()

        self.node_map = NodeMap(
            pos=(WIDTH / 2 / RENDER_SCALE, HEIGHT / 2 / RENDER_SCALE),
            size=16,
            row=0,
            col=0,
        )
        self.node_map.load("maps/69.json")

        self.agent = Agent(self.node_map)
        self.frame = 0

    def run(self):
        running = True
        while running:
            # For Background ------------------------------------------------------|
            self.display.fill(BG_COLOR)

            self.node_map.draw(self.display)
            if self.frame % 8 == 0:
                # self.agent.move_random()
                self.agent.a_star()
            self.agent.draw(self.display)

            # Checking Events -----------------------------------------------------|
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.node_map.load("maps/69.json")
                        self.agent = Agent(self.node_map)

                if event.type == pygame.KEYUP:
                    pass

            # Rendering Screen ----------------------------------------------------|
            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )
            pygame.display.update()
            self.clock.tick(60)
            self.frame += 1


if __name__ == "__main__":
    Game().run()
    # Quit --------------------------------------------------------------------|
    print("Game Over")
    pygame.quit()
    sys.exit()
    exit()
