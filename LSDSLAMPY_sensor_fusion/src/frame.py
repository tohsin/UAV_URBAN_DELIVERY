import imp
from tkinter import Widget
import numpy as np
import cv2 as cv
from framepose import FramePose



class  Frame:
    
    def __init__(self, id : int  = None,  width : int = None, height : int = None, K: np.ndarray = None, timestamp: float = None,
    image = None) -> None:
        self.data = Data()
        self.initialise(id, width=width, height=height,K= K,timestamp=timestamp)

    def initialise(self, id, width, height, K, timestamp):
        self.data.id = id
        self.pose = FramePose()
        self.data.K[0] = 


