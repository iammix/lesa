import numpy as np

from domain import Element


class Spring(Element):
    """
    ADD DOCSTRINGS
    """

    def __init__(self, nodes, ke):
        Element.__init__(self, element_type='spring')
        self.nodes = nodes
        self.k = ke

    def get_element_stiffness(self):
        self._KE = np.array([[self.k, -self.k], [-self.k, self.k]])
        return self._KE

    def get_global_stiffness(self, msz):
        pass

    def get_nodes(self):
        return self.nodes


class Bar(Element):
    def __init__(self, nodes, E, A):
        super().__init__(self, element_type='bar')
        self.node = nodes
        self.E = E
        self.A = A

    def fx(self):
        ke = self.get_element_stiffness()
        n1, n2 = self.get_nodes()
        un = np.array([n1.ux], [n2.ux])
        return np.dot(ke, un)

    def set_fx(self, fx):
        self._fx = fx

    def sx(self):
        ke = self.get_element_stiffness()
        na, nb = self.get_nodes()
        u = np.array([na.ux, nb.ux])
        sx = np.dot(ke, u / self.A)
        return sx

    def set_sx(self, sx):
        self._sx = sx

    def L(self):
        ni, nj = self.get_nodes()
        x0, x1, y0, y1 = ni.x, nj.x, ni.y, nj.y
        _l = np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
        return _l

    def get_element_stiffness(self):
        self._KE = (self.A * self.E / self.L) * np.array([[1, -1], [-1, 1]])
        return self._KE

    def get_nodes(self):
        return self.nodes
