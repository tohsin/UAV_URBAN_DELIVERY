from tkinter.messagebox import RETRY
import g2o
class FramePose:
    _cacheValidCounter  = 0
    def __init__(self) -> None:
        self.trackingParent : FramePose = None
        # whether this poseStruct is registered in the Graph. if true MEMORY WILL BE HANDLED BY GRAPH
        self.isRegisteredToGraph : bool
        self.graphVertex : g2o.Sim3()
        self.isOptimized : bool
        self.camToWorld : g2o.Sim3()
        self._cacheValidFor  : int
        self.thisToParent_raw : g2o.Sim3()
        


    def getCamToWorld(self, recursionDepth = 0) -> g2o.Sim3():
        # if the node is in the graph, it's absolute pose is only changed by optimization.
        if self.isOptimized : 
            return self.camToWorld

        #return chached pose, if still valid.
        if(self._cacheValidFor ==  FramePose.cacheValidCounter):
            return self.camToWorld

        #return id if there is no parent (very first frame)
        if(self.trackingParent == None):
            self.camToWorld = g2o.Sim3()
            return self.camToWorld

        # abs. pose is computed from the parent's abs. pose, and cached.
        self.cacheValidFor = FramePose.cacheValidCounter
        self.camToWorld = self.trackingParent.getCamToWorld(recursionDepth+1) *self.thisToParent_raw
        return self.camToWorld


	