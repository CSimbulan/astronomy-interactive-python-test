import pylab as p
import numpy as np
import astropy.io.fits as pf

def cutOff(data, s):
    std = np.std(data)
    bright = np.where(data > s*std)
    return bright

coords = []
xcoords = []
ycoords = []
centroids = []
x, y = 0, 0
def match(x, y):
    global xcoords
    global ycoords
    global xc
    global yc
    if (x,y) not in coords:
        xcoords.append(float(x))
        ycoords.append(float(y))
        coords.append((x,y))
        print str((x, y)) + " Taken!"
    else:
        xc = sum(xcoords)/len(xcoords)
        yc = sum(ycoords)/len(ycoords)
        print "Centroid found at: " + str((xc, yc))
        centroids.append((xc, yc))
        p.plot(xc, yc, '.r')
        xcoords = []
        ycoords = []
    return None


class Interactive(object):

    def __init__(self, data, x, y, tolerance = 5, formatter = match):
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
            
a = pf.open("NGC.fts")
b = cutOff(a[0].data, 40.0)

plot = p.plot(b[1], b[0], '.b')
Interactive(plot, b[1], b[0])

p.imshow(a[0].data, cmap='gray')

p.colorbar()
p.show()
