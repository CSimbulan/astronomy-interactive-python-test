import pylab as p
import numpy as np

coords1 = []
coords2 = []
p1 = []
p2 = []
count = 0
def match(x, y):
    global p1
    global p2
    global count
    if count < 2:
        p1.append(x)
        p2.append(y)
        count += 1
    if count == 2:
        p.plot(p1, p2)
        count = 0
        coords1.append((p1[0], p2[0]))
        coords2.append((p1[1], p2[1]))
        print "Matched " + str((p1[0], p2[0])) + " with " + str((p1[1], p2[1]))
        p1 = []
        p2 = []
    return None

class Interactive(object):

    def __init__(self, data, x = [], y = [], tolerance = 5, formatter = match):
        self._points = np.column_stack((x,y))
        self.formatter = formatter
        if not p.iterable(data):
            data = [data]
        self.data = data
        self.axes = tuple(set(d.axes for d in self.data))
        self.figures = tuple(set(ax.figure for ax in self.axes))
        for d in self.data:
            d.set_picker(tolerance)
        for fig in self.figures:
            fig.canvas.mpl_connect('pick_event', self)
    def snap(self, x, y):
        idx = np.nanargmin(((self._points - (x,y))**2).sum(axis = -1))
        return self._points[idx]
    def __call__(self, event):
        x, y = event.mouseevent.xdata, event.mouseevent.ydata
        if x is not None:
            x, y = self.snap(x, y)
            self.formatter(x,y)
            event.canvas.draw()





xdots = [1,1,2,3,5,8,13]
ydots = [5,-3,4,12,10,11, 7]
xdots2 = list((np.array(xdots)*1.002) + 0.3)
ydots2 = list((np.array(ydots)*1.001) + 0.2)
plot = p.scatter(xdots, ydots), p.scatter(xdots2, ydots2, color='red')
Interactive(plot, xdots+xdots2, ydots+ydots2)
p.show()
