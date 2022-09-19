import g2o
import numpy as np
from TrackingRefrence import TrackingReference
from frame import Frame
from LGSX import    LGS7,LGS6,LGS4
from util.settings import DenseDepthTrackerSettings
PYRAMID_LEVELS = 5

class Sim3ResidualStruct():

	float sumResD
	float sumResP;
	int numTermsD;
	int numTermsP;

	float meanD;
	float meanP;
	float mean;
	
	inline Sim3ResidualStruct()
	{
		meanD = 0;
		meanP = 0;
		mean = 0;
		numTermsD = numTermsP = sumResD = sumResP = 0;
	}
};


class Sim3Tracker():
    def __init__(self, w: int, h : int, K : np.ndarray) -> None:
        self.width = w 
        self.height = h 
        # camera intrisics
        self.K = K
        self.Kinv = np.linalg.inv(K) # inverse intristics
        self.fx = K[0,0]
        self.fy = K[1,1]
        self.cx = K[0,2]
        self.cy = K[1,2]

        self.fxi = self.Kinv[0,0]
        self.fyi = self.Kinv[1,1]
        self.cxi = self.Kinv[0,2]
        self.cyi = self.Kinv[1,2]

        self.lastSim3Hessian = np.zeros((7,7))

        self.lastResidual = 0
        self.iterationNumber = 0
        self.lastDepthResidual = self.lastPhotometricResidual = self.lastDepthResidualUnweighted = self.lastPhotometricResidualUnweighted = self.lastResidualUnweighted = 0
        self.pointUsage = 0

        self.settings : DenseDepthTrackerSettings

    def trackFrameSim3(self, reference : TrackingReference,
                        frame : Frame, 
                        frameToReference_initialEstimate : g2o.Sim3() ,
                        startLevel : int, 
                        finalLevel : int):
        referenceToFrame = frameToReference_initialEstimate.inverse()
        ls7 : LGS7
        numCalcResidualCalls = [0] * PYRAMID_LEVELS
        numCalcWarpUpdateCalls = [0] * numCalcWarpUpdateCalls

        finalResidual : Sim3ResidualStruct 
        warp_update_up_to_date = False

        for lvl in range(startLevel , finalLevel -1 , -1):
            numCalcResidualCalls[lvl] = 0
            numCalcWarpUpdateCalls[lvl] = 0

            if(self.settings.maxItsPerLvl[lvl] == 0) : continue
            reference.makePointCloud(lvl)

            

            



