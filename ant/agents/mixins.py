"""
Module mixins
****

:Author: tobijjah
:Date: 02.06.19
"""


class AlphaGradient:
    def get_alpha(self, x):
        return ((x - self._xmin) / (self._xmax - self._xmin)) * (self._ymax - self._ymin)


class ColorGradientMixin:
    def get_gradient(self, value):
        if value > 1:
            value = 1

        return [
            self._start_color[idx] + value * (self._end_color[idx] - self._start_color[idx])
            for idx in range(3)
        ]
