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


class Truss(Element):
    def __init__(self, nodes, E, A):
        super().__init__(self, element_type='truss')
        self.nodes = nodes
        self.E = E
        self.A = A

    def length(self):
        ni, nj = self.get_nodes()
        x0, x1, y0, y1 = ni.x, nj.x, ni.y, nj.y
        _l = np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
        return _l

    def theta(self):
        ni, nj = self.get_nodes()
        x0, x1, y0, y1 = ni.x, nj.x, ni.y, nj.y
        theta = np.arctan2((y1 - y0), (x1 - x0))
        return theta

    def force(self):
        return self._compute_force()

    def stress(self):
        s = self.force / self.A
        return s

    def _compute_force(self):
        E, A, L = self.E, self.A, self.L
        c = np.cos(self.theta)
        s = np.sin(self.theta)
        ni, nj = self.get_nodes()
        u = np.array([ni.ux, ni.uy, nj.ux, nj.uy])
        F = (E * A / L) * np.dot(np.array([-c, -s, c, s]), u)
        return F

    def get_element_stiffness(self):
        c = np.cos(self.theta)
        s = np.sin(self.theta)
        cs = c * s
        self._K = (self.E * self.A / self.L) * np.array([[c ** 2, cs, -c ** 2, -cs],
                                                         [cs, s ** 2, -cs, -s ** 2],
                                                         [-c ** 2, -cs, c ** 2, cs],
                                                         [-cs, -s ** 2, cs, s ** 2]])

    def get_nodes(self):
        return self.nodes


class Beam(Element):
    def __init__(self, nodes, E, I):
        super().__init__(self, element_type='beam')
        self.nodes = nodes
        self.E = E
        self.I = I

    def get_element_stiffness(self):
        coef1 = 2 * self.L ** 2
        coef2 = 4 * self.L ** 2
        coef3 = 6 * self.L
        self._K = (self.E * self.I / self.L) * np.array([[12, coef3, -12, coef3],
                                                         [coef3, coef2, -coef3, coef1],
                                                         [-12, -coef3, 12, -coef3],
                                                         [coef3, coef1, -coef3, coef2]])
        return self._K

    def _compute_element_forces(self):
        ke = self.get_element_stiffness()
        n1, n2 = self.get_nodes()
        un = np.array([[n1.uy, n1.ur, n2.uy, n2.ur]]).transpose()
        EF = np.dot(ke, un)
        self.fy = EF[::2]
        self.m = EF[1::2]

    def fy(self):
        self._compute_element_forces()
        return self._fy

    def set_fy(self, fy):
        self._fy = fy

    def m(self):
        self._compute_element_forces()
        return self._m

    def set_m(self, m):
        self._m = m

    def L(self):
        ni, nj = self.get_nodes()
        x0, x1, y0, y1 = ni.x, nj.x.ni.y, nj.y
        _l = np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
        return _l

    def get_nodes(self):
        return self.nodes

class Triangle(Element):
    def __init__(self, nodes, E, nu, t):
        super().__init__(self, element_type='triangle')
        self.nodes = nodes
        self.E = E
        self.nu = nu
        self.t = t
        self._sx = 0
        self._sy = 0
        self._sxy = 0
    def sx(self):
        _sx,_sy,_sxy = self.get_element_stresses()
        self._sx = _sx

    def set_sx(self, sx):
        self._sx = sx

    def sy(self):
        _sx, _sy,_sxy = self.get_element_stresses()
        self._sy = _sy
        return self._sy

    def set_sy(self, sy):
        self._sy = sy

