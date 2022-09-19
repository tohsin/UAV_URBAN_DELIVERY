class B:
    def __init__(self) -> None:
        self.time = 0

class Graph:
    def __init__(self) -> None:
        self.graph_ =[B] * 3

    def addnode(self, b :B):
        self.graph_.append(b.time)
b = B()
print(b.time)
def compute(val_ : B):
    val_.time = 8

compute(b)
print(b.time)