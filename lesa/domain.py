import numpy as np

class Model:
    def __init__(self,args):
        pass
    
class Element:
    def __init__(self, args):
        pass
    
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
        # Nodal stresses
        self._sx = 0.0
        self._sy = 0.0
        self._sxy = 0.0
        self._seqv = 0.0
        self.con_elements = []
        
    
    def label(self):
        return self.label