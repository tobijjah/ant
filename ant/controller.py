"""
controller
**********

:Author: tobijjah
:Date: 03.06.19
"""
import sys

import pygame
from affine import Affine
from pygame.locals import *

from ant.environment import Environment


class Controller:
    def __init__(self, screen_size, field_size, neighbours, torus, nutrients, ant_type):
        self.screen, self.background, self.transform = self.init_display(screen_size, field_size)
        self.clock = pygame.time.Clock()

        self.size = nutrients

        self.nature = self.init_nature(field_size, neighbours, torus)
        self.ants = list()  # Later Ant monitor
        self.holes = list()  # LAte Holes monitor
        self.nutrients = list()  # Later Nutrients monitor
        self.pheromones = list()  # Later Pheromone monitor
        self.selected_cell = None

    def init_display(self, screen_size, field_size):
        pygame.init()

        screen = pygame.display.set_mode(screen_size)
        background = pygame.Surface((screen.get_width(), screen.get_height()))
        transform = Affine(
            screen_size[0] / field_size[1], 0, 0,
            0, screen_size[1] / field_size[0], 0
        )

        return screen, background, transform

    def init_nature(self, field_size, neighbours, torus):
        return Environment(self.transform, self.background, field_size, neighbours, torus)

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                self.handle_select(event)

            elif event.type == KEYDOWN:
                self.handle_keydown(event)

    def handle_select(self, event):
        cell = self.nature.get_display_cell(event)

        if self.selected_cell:
            self.selected_cell.set_selected()

        self.selected_cell = cell
        self.selected_cell.set_selected()

    def handle_keydown(self, event):
        if self.selected_cell and not self.selected_cell.occupied():
            if event.unicode == 'h':
                cell = self.selected_cell.spawn_hole()
                self.holes.append(cell)

            elif event.unicode == 'n':
                cell = self.selected_cell.spawn_nutrient(self.size)
                self.nutrients.append(cell)

            elif event.unicode == 'o':
                # spawn obstacle
                # requires new class obstacle (is lightweight)
                # requires a obstacle filter in allowed cells in ant method
                pass

        if self.selected_cell and self.selected_cell.has_hole():
            # later ant type
            if event.unicode == 'a':
                ant = self.selected_cell.spawn_ant()
                self.ants.append(ant)

        if self.selected_cell and self.selected_cell.occupied():
            if event.unicode == 'd':
                del self.selected_cell.hole
                del self.selected_cell.nutrient
                # del self.selected_cell.obstacle

    def run(self):
        hole = self.nature.spawn_hole()
        self.nutrients = [self.nature.spawn_nutrient(amount=10000) for i in range(1)]
        self.ants = [hole.spawn_ant() for i in range(1)]

        while True:
            self.clock.tick(10)
            self.event_loop()

            for ant in self.ants:
                ant.collide(self.nutrients + self.holes)
                ant.move(self.nature.visible(ant))

            self.nature.draw()
            [ant.draw() for ant in self.ants]

            self.screen.blit(self.background, self.background.get_rect())
            pygame.display.update()
