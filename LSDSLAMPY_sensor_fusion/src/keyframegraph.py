
import numpy as np
import sophus as sp
from frame import Frame
import g2o
from framepose import FramePose
from threading import Thread, Lock
from liealgebra__.sim3 import SIM3
import g2o

class KFConstraint():
    def __init__(self) -> None:
        self.firstFrame : Frame
        self.secondFrame : Frame
        self.information = np.zeros((7,7))
        self.edge = g2o.EdgeSim3()
        self.secondToFirst = g2o.Sim3()
        self.usage : float
        self.meanResidualD : float
        self.meanResidualP : float
        self.meanResidual : float
        self.reciprocalConsistency : float
        self.idxInAllEdges : int

class KeyFrameGraph():
    def __init__(self, nextEdgeId = 0 ) -> None:
        self.poselock = Lock()
        self.edgesListsMutex = Lock()
        self.allFramePoses = []
        self.optimizer = g2o.SparseOptimizer()
        
        self.newKeyframesBuffer = []
        self.newEdgeBuffer = []
        self.edgesAll = []
        
        self.solver = g2o.BlockSolverSim3(g2o.LinearSolverCSparseSim3())
        self.solver = g2o.OptimizationAlgorithmLevenberg(self.solver)
        
        self.optimizer.set_algorithm(self.solver)
        

        self.optimizer.set_verbose(False)
        self.totalPoints=0
        self.totalEdges=0
        self.totalVertices=0

        self.nextEdgeId  = nextEdgeId

    def addFrame(self, frame : Frame ):
        frame.pose.isRegisteredToGraph = True
        pose = frame.pose.copy()
        self.poselock.acquire()
        self.allFramePoses.append(pose)
        self.poselock.release()

    def addKeyFrame(self, frame : Frame):
        if (frame.pose.graphVertex != None):
            return
        vertex  =  g2o.VertexSim3Expmap()
        vertex.set_id(frame.getId)
        camToWorld_estimate : g2o.Sim3()
        camToWorld_estimate = frame.getScaledCamToWorld()

        if (not frame.hasTrackingParent()):
            vertex.set_fixed(True)
        vertex.set_estimate(camToWorld_estimate)
        vertex.set_marginalized(False)
        frame.pose.graphVertex = vertex
        self.newKeyframesBuffer.append(frame)

    def optimise(self, num_iterations : int):
        if (len(self.optimizer.edges())== 0):
            return 0
        self.optimizer.set_verbose(False); # printOptimizationInfo
        self.optimizer.initialize_optimization()
        return self.optimizer.optimize(num_iterations, False)
    
    def insertConstraint(self, constraint : KFConstraint):
        edge = g2o.EdgeSim3()
        self.nextEdgeId+=1
        self.totalEdges+=1

        edge.set_measurement(constraint.secondToFirst)
        edge.set_information(constraint.information)
        edge.set_robust_kernel(g2o.RobustKernelHuber())
        edge.resize(2)

        assert(constraint.firstFrame.pose.graphVertex != None)
        edge.set_vertex(0, constraint.firstFrame.pose.graphVertex)
        assert(constraint.secondFrame.pose.graphVertex != None)
        edge.set_vertex(1, constraint.secondFrame.pose.graphVertex)
        constraint.edge = edge

        self.newEdgeBuffer.append(constraint)

        constraint.firstFrame.neighbors.add(constraint.secondFrame)
        constraint.secondFrame.neighbors.add(constraint.firstFrame)

        self.edgesListsMutex.acquire()
        constraint.idxInAllEdges = self.edgesAll.size()
        self.edgesAll.append(constraint)
        self.edgesListsMutex.release()



        

        
    
class PoseGraphOptimization(g2o.SparseOptimizer):
    def __init__(self):
        super().__init__()
        
        solver = g2o.BlockSolverSE3(g2o.LinearSolverCholmodSE3())
        solver = g2o.OptimizationAlgorithmLevenberg(solver)
        super().set_algorithm(solver)

    def optimize(self, max_iterations=30):
        super().initialize_optimization()
        super().set_verbose(True)
        super().optimize(max_iterations)

    def add_vertex(self, id, pose, fixed=False):
        v_se3 = g2o.VertexSE3()
        v_se3.set_id(id)
        v_se3.set_estimate(pose)
        v_se3.set_fixed(fixed)
        super().add_vertex(v_se3)

    def add_edge(self, vertices, measurement, 
            information=np.identity(6),
            robust_kernel=None):

        edge = g2o.EdgeSE3()
        for i, v in enumerate(vertices):
            if isinstance(v, int):
                v = self.vertex(v)
            edge.set_vertex(i, v)

        edge.set_measurement(measurement)  # relative pose
        edge.set_information(information)
        if robust_kernel is not None:
            edge.set_robust_kernel(robust_kernel)
        super().add_edge(edge)

    def get_pose(self, id):
        return self.vertex(id).estimate()

