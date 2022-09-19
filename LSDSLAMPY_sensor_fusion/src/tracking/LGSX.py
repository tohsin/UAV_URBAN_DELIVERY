import numpy as np

class LGS6():
    def __init__(self) -> None:
        self.A = np.zeros((6,6)) # hesseian
        self.b = np.zeros((6,1)) # bias
        self.num_constraints : int
    
class LGS4():
    def __init__(self) -> None:
        self.A = np.zeros((6,6)) # hesseian
        self.b = np.zeros((6,1)) # bias
        self.num_constraints: int
    
class LGS7():
    def __init__(self) -> None:
        self.A = np.zeros((7,7)) # hesseian
        self.b = np.zeros((7,1)) # bias
        self.error : float
        num_constraints : int

    def initializeFrom(self, ls6 : LGS6, ls4 : LGS4):

        # set zeros
        self.A = np.zeros((7,7)) # hesseian
        self.b = np.zeros((7,1)) # bias

        # add ls6
        self.A[0:6, 0:6] = ls6.A
        self.b[0:6] = ls6.b

        #add ls4
        remap = [2,3,4,6]
        for i in range(4):
            self.b[remap[i]] += ls4.b[i]
            for j in range(4):
                self.A[remap[i], remap[j]] += ls4.A[i,j]

        self.num_constraints = ls6.num_constraints + ls4.num_constraints

