"""
Module monitor
****

:Author: tobijjah
:Date: 02.06.19
"""


class PheromoneMonitor:
    def __init__(self, environment):
        environment.on_pheromone.connect(self.add_cell)
        self.monitored_cell = []

    def add_cell(self, cell):
        self.monitored_cell.append(cell)

    def run(self):
        intensities = [cell.pheromone.intensity for cell in self.monitored_cell]

        if intensities:
            min_intensity = min(intensities)
            max_intensity = max(intensities)

            print(min_intensity, max_intensity)
