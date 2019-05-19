import pylab as p
import numpy as np

coords = []
def click(x, y):
    global count
    if (x,y) not in coords:
        p.plot(x, y, 'or')
        coords.append((x, y))
        print "Peak found at " + str((x, y))
    else:
        print "Point already selected!"
    return None

class Interactive(object):

    def __init__(self, data, x = [], y = [], tolerance = 5, formatter = click):
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



xdata, ydata = np.loadtxt('peaks.txt',delimiter=',', unpack=True)
plot = p.plot(xdata, ydata)
Interactive(plot, xdata, ydata)

p.show()
