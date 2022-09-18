import imp
from tkinter import Widget
import numpy as np
import cv2 as cv
from framepose import FramePose
from data import Data

PYRAMID_LEVELS = 5

class  Frame:
    
    def __init__(self, id : int  = None,  width : int = None, height : int = None, K: np.ndarray = None, timestamp: float = None,
    image = None) -> None:
        self.data = Data()
        self.depthHasBeenUpdatedFlag : bool
        self.referenceID : int
        self.referenceLevel : int
        self.numMappablePixels : int
        self.initialise(id, width=width, height=height,K= K,timestamp=timestamp)

    def initialise(self, id, width, height, K: np.ndarray , timestamp):
        self.data.id = id
        self.pose = FramePose()
        self.data.K[0] = K
        
        self.data.fx[0] = K[0, 0]
        self.data.fy[0] = K[1, 1]
        self.data.cx[0] = K[0, 2]
        self.data.cy[0] = K[1, 2]

        self.data.KInv[0] = np.linalg.inv(K)
        self.data.fxInv[0] = self.data.KInv[0][0, 0]
        self.data.fyInv[0] = self.data.KInv[0][1, 1]
        self.data.cxInv[0] = self.data.KInv[0][0, 2]
        self.data.cyInv[0] = self.data.KInv[0][1, 2]

        self.data.timestamp = timestamp

        self.data.hasIDepthBeenSet = False
        self.depthHasBeenUpdatedFlag = False

        self.referenceID = -1
        self.referenceLevel = -1
	
        self.numMappablePixels = -1

        for level in range(0, PYRAMID_LEVELS):
            self.data.width[level] = width >> level
            self.data.height[level] = height >> level
            self.data.imageValid[level] = False
            self.data.gradientsValid[level] = False
            self.data.maxGradientsValid[level] = False
            self.data.idepthValid[level] = False
            self.data.idepthVarValid[level] = False
            
            self.data.image[level] = 0
            self.data.gradients[level] = 0
            self.data.maxGradients[level] = 0
            self.data.idepth[level] = 0
            self.data.idepthVar[level] = 0
            self.data.reActivationDataValid = False

            if (level > 0):
                self.data.fx[level] = self.data.fx[level-1] * 0.5
                self.data.fy[level] = self.data.fy[level-1] * 0.5
                self.data.cx[level] = (self.data.cx[0] + 0.5) / (1<<level) - 0.5
                self.data.cy[level] = (self.data.cy[0] + 0.5) / (1<<level) - 0.5

                self.data.K[level]  << self.data.fx[level], 0.0, self.data.cx[level], 0.0, self.data.fy[level], data.cy[level], 0.0, 0.0, 1.0;	// synthetic
                data.KInv[level] = (data.K[level]).inverse();

                data.fxInv[level] = data.KInv[level](0,0);
                data.fyInv[level] = data.KInv[level](1,1);
                data.cxInv[level] = data.KInv[level](0,2);
                data.cyInv[level] = data.KInv[level](1,2);

        

    def width(self, level : int ):
        return self.data.width[level]

    def height(self, level : int):
        return self.data.height[level]

    def K(self):
        pass


