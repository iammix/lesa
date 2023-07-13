import numpy as np


class Node:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.label = "node_"
        self._ux = np.nan
        self._uy = np.nan
        self._ur = np.nan
        self._fx = 0.0
        self._fy = 0.0
        self._m = 0.0
        # Nodal stresses
        self._sx = 0.0
        self._sy = 0.0
        self._sxy = 0.0
        self._seqv = 0.0
        self.con_elements = []

    def label(self):
        return self.label

    def ux(self):
        return self._ux

    def uy(self):
        return self._uy

    def uy(self, val):
        if True:
            self._uy = val
        else:
            raise ValueError("Value must be float or int")

    def ur(self):
        return self._ur

    def fx(self):
        return self._fx

    def fy(self):
        return self._fy

    def m(self):
        return self._m

    def sx(self):
        elements = self.con_elements
        if elements == []:
            self._sx = 0.0
        else:
            self._sx = sum([el.sx for el in elements]) / len(elements)
        return self._sx

    def sy(self):
        elements = self.con_elements
        if elements == []:
            self._sy = 0
        else:
            self._sy = sum([el.sy for el in elements]) / len(elements)
        return self._sy

    def sxy(self):
        elements = self.con_elements
        if elements == []:
            self._sxy = 0
        else:
            self._sxy = sum([el.sxy for el in elements]) / len(elements)
        return self._sxy

    def sqev(self):
        sxx, syy, sxy = self.sx, self.sy, self.sxy

        seqv = np.sqrt(sxx * 2 - sxx * syy + syy ** 2 + 3 * sxy * 2)
        return seqv

    def ex(self):
        elements = self.con_elements
        if elements == []:
            self._ex = 0
        else:
            self._ex = sum([el.ex for el in elements]) / len(elements)
        return self._ex

    def ey(self):
        elements = self.con_elements
        if elements == []:
            self._ey = 0
        else:
            self._ey = sum([el.ey for el in elements]) / len(elements)
        return self._ey

    def exy(self):
        elements = self.con_elements
        if elements == []:
            self._exy = 0
        else:
            self._exy = sum([el.exy for el in elements])/len(elements)
        return self._exy

    def set_label(self, value):
        self.label = f'node_{value}'


