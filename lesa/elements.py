import numpy as np
from domain import Element
from scipy.sparse import csr_matrix

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