PYRAMID_LEVELS = 5
class DenseDepthTrackerSettings:
    def __init__(self) -> None:
        self.maxItsPerLvl = [0] * PYRAMID_LEVELS