
from showresult.Circle import CircleDraw

class CircleDrawTest:
    def __init__(self):
        self.circle = CircleDraw()

    def testbing(self):
        self.circle.draw()


if __name__ == '__main__':
    cDraw = CircleDraw()
    cDraw.draw()