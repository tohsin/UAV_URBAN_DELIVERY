from ast import Set
import imp
import numpy as np
import cv2 as cv
from LSDSLAMPY_sensor_fusion.src.liealgebra__ import sim3
from framepose import FramePose
from data import Data
from liealgebra__.sim3 import SIM3

PYRAMID_LEVELS = 5

class  Frame:
    
    def __init__(self, id : int  = None,  width : int = None, height : int = None, K: np.ndarray = None, timestamp: float = None,
    image = None) -> None:
        self.data = Data()
        self.depthHasBeenUpdatedFlag : bool
        self.referenceID : int
        self.referenceLevel : int
        self.numMappablePixels : int
        self.lastConstraintTrackedCamToWorld  : SIM3
        self.isActive : False
        self.permaRefNumPts : int
        self.permaRef_colorAndVarData  : int
        self.permaRef_posData : int
        self.meanIdepth : int
        self.numPoints  : int
        self.pose : FramePose
        self.neighbors = set()
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
        '''
        k = fx 0 cx refer to xiang book
            0 fy cy
            0 0  1
        '''
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

                self.data.K[level] =np.array([self.data.fx[level], 0.0, self.data.cx[level], 
                                            0.0, self.data.fy[level], self.data.cy[level], 
                                            0.0, 0.0, 1.0])

                self.data.KInv[level] = np.linalg.inv(self.data.K[level])

                self.data.fxInv[level] = self.data.KInv[level][0,0]
                self.data.fyInv[level] = self.data.KInv[level][1,1]
                self.data.cxInv[level] = self.data.KInv[level][0,2]
                self.data.cyInv[level] = self.data.KInv[level][1,2]


        self.data.validity_reAct = 0
        self.data.idepthVar_reAct = 0
        self.data.idepth_reAct = 0

        self.data.refPixelWasGood = 0

        self.permaRefNumPts = 0
        self.permaRef_colorAndVarData = 0
        self.permaRef_posData = 0

        self.meanIdepth = 1
        self.numPoints = 0

        self.numFramesTrackedOnThis = self.numMappedOnThis = self.numMappedOnThisTotal = 0

        self.idxInKeyframes = -1

        self.edgeErrorSum = self.edgesNum = 1

        self.lastConstraintTrackedCamToWorld = SIM3()

        self.isActive = False;             
    
    def __hash__(self) -> int:
        return self.getId()
    def getScaledCamToWorld(self):
        return self.pose.getCamToWorld()
    def getWidth(self, level : int ):
        return self.data.width[level]

    def hasTrackingParent(self):
        return (self.pose.trackingParent != None)

    def getHeight(self, level : int):
        return self.data.height[level]

    def getK(self):
        pass
    def getId(self):
        return self.data.id


