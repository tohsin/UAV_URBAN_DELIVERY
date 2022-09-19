import numpy as np
class Data:
    def __init__(self) -> None:
        self.id = None
        self.width = None; self.height = None
        
        self.K = [ np.ndarray ] * 5 # camera intristics per level of 3,3 matrix
        # camera intristics inverse per level of 3,3 matrix
        self.KInv = [0] * 5
        self.fx = [0] * 5; self.fy = [0] * 5; self.cx = [0] * 5; self.cy = [0] * 5
        self.fxInv = None; self.fyInv = None; self.cxInv = None; self.cyInv = None
        self.timestamp = None

       

        self.imageValid : bool = [False] * 5
        self.gradientsValid : bool = [False] * 5
        self.maxGradientsValid = [False] *5
        self.idepthValid = [False] *5
        self.idepthVarValid = [False] * 5


        self.image = [0] * 5
        self.gradients = [0] * 5 
       
        self.hasIDepthBeenSet = None
        self.maxGradients = [0.0] * 5
        self.idepth = [0.0] * 5
        self.idepthVar = [0.0] * 5
        self.reActivationDataValid : bool 
        

        # data from initial tracking, indicating which pixels in the reference frame ware good or not.
		# deleted as soon as frame is used for mapping.
        self.refPixelWasGood : bool
        self.validity_reAct : int
        self.idepthVar_reAct : int
        self.idepth_reAct : int