import numpy as np
class Data:
    def __init__(self) -> None:
        self.id = None
        self.width = None; self.height = None
        self.K = [0] * 5 ; self.Kinv = [0] * 5
        self.fx = [0] * 5; self.fy = [0] * 5; self.cx = [0] * 5; self.cy = [0] * 5
        self.fxinv = None; self.fyinv = None; self.cxinv = None; self.cyinv = None
        self.timestamp = None
        self.image = None
        self.imageValid : bool = None
        self.gradients = None 
        self.gradientsValid : bool = None
        self.gradients = None
        self.gradients = None 
        self.gradients = None
        self.gradients = None

        self.fx = None