import os
import math
import struct
import Quartz.CoreGraphics as CG
from AppKit import NSScreen


class ScreenPixel(object):
    def __init__(self, top, right, bottom, left, height, width, offsetTop, offsetRight, offsetBottom, offsetLeft, step):
        self.lights = (top, right, bottom, left)
        self.area = (height, width)
        self.offset = (offsetTop, offsetRight, offsetBottom, offsetLeft)
        self.screenSizes = (
            NSScreen.mainScreen().frame().size.height,
            NSScreen.mainScreen().frame().size.width
        )
        self.step = step
    
    def getBrightness(self):
        command = 'ioreg -c AppleBacklightDisplay | grep brightness'
        result = os.popen(command).read()
        result = result.split('"brightness"={')[1].split('}')[0].split(',')
        
        maxValue = float(result[1].split('=')[1])
        value = float(result[2].split('=')[1])
        
        return int(math.ceil(value * 100 / maxValue))
    
    def getRatio(self):
        return 2
    
    def capture(self, region = None):
        if region is None:
            region = CG.CGRectInfinite
        else:
            if region.size.width % 2 > 0:
                emsg = "Capture region width should be even (was %s)" % (
                    region.size.width)
                raise ValueError(emsg)

        image = CG.CGWindowListCreateImage(
            region,
            CG.kCGWindowListOptionOnScreenOnly,
            CG.kCGNullWindowID,
            CG.kCGWindowImageDefault)

        prov = CG.CGImageGetDataProvider(image)

        self._data = CG.CGDataProviderCopyData(prov)

        self.width = CG.CGImageGetWidth(image)
        self.height = CG.CGImageGetHeight(image)

    def pixel(self, x, y):
        """
        Must call capture first.
        """

        data_format = "BBBB"
        
        offset = 4 * ((self.width*int(round(y))) + int(round(x)))

        b, g, r, a = struct.unpack_from(data_format, self._data, offset=offset)

        return (r, g, b)
        return (r, g, b, a)
    
    def getRegion(self, x1, y1, x2, y2):
        return CG.CGRectMake(x1, 1, x2, y2)
    
    
    def getColorsX(self, lights, x1, y1, x2, y2):
        x1 = int(x1 * self.getRatio())
        y1 = int(y1 * self.getRatio())
        x2 = int(x2 * self.getRatio())
        y2 = int(y2 * self.getRatio())
        
        ret = [ [0] * 3 ] * lights
        for light in range(lights):
            r = 0
            g = 0
            b = 0
            
            i_start = int(x1 + light * ((x2 - x1) / lights))
            i_stop = int(x1 + (light + 1) * ((x2 - x1) / lights))
            
            n = len(range(i_start, i_stop, self.step)) * len(range(y1, y2, self.step))
            
            for i in range(i_start, i_stop, self.step):
                for j in range(y1, y2, self.step):
                    pixel = self.pixel(i, j)
                    r += float(pixel[0]) / n
                    g += float(pixel[1]) / n
                    b += float(pixel[2]) / n
            ret[light] = [int(r), int(g), int(b)]
        return ret
    def getColorsY(self, lights, x1, y1, x2, y2):
        x1 = int(x1 * self.getRatio())
        y1 = int(y1 * self.getRatio())
        x2 = int(x2 * self.getRatio())
        y2 = int(y2 * self.getRatio())
        
        ret = [ [0] * 3 ] * lights
        for light in range(lights):
            r = 0
            g = 0
            b = 0
            
            j_start = int(y1 + light * (y2 - y1) / lights)
            j_stop = int(y1 + (light + 1) * (y2 - y1) / lights)
            
            n = len(range(x1, x2, self.step)) * len(range(j_start, j_stop, self.step))
            
            for i in range(x1, x2, self.step):
                for j in range(j_start, j_stop, self.step):
                    pixel = self.pixel(i, j)
                    r += float(pixel[0]) / n
                    g += float(pixel[1]) / n
                    b += float(pixel[2]) / n
            ret[light] = [int(r), int(g), int(b)]
        return ret
    
    def getColorsTop(self):
        x1 = self.offset[3]
        y1 = 0
        x2 = self.screenSizes[1] - self.offset[1]
        y2 = self.area[0]
        
        return self.getColorsX(self.lights[0], x1, y1, x2, y2)
    def getColorsBottom(self):
        x1 = self.offset[3]
        y1 = self.screenSizes[0] - self.area[0]
        x2 = self.screenSizes[1] - self.offset[1]
        y2 = self.screenSizes[0]
        
        return self.getColorsX(self.lights[2], x1, y1, x2, y2)
    
    def getColorsRight(self):
        x1 = self.screenSizes[1] - self.area[1]
        y1 = self.offset[0]
        x2 = self.screenSizes[1]
        y2 = self.screenSizes[0] - self.offset[2]
        
        return self.getColorsY(self.lights[1], x1, y1, x2, y2)
    
    def getColorsLeft(self):
        x1 = 0
        y1 = self.offset[0]
        x2 = self.area[1]
        y2 = self.screenSizes[0] - self.offset[2]
        
        return self.getColorsY(self.lights[3], x1, y1, x2, y2)
    
    def getColors(self):
        ret = []
        self.capture()
        
        ret.append(self.getColorsTop())
        ret.append(self.getColorsRight())
        ret.append(self.getColorsBottom())
        ret.append(self.getColorsLeft())
        return ret
    def getColorsHex(self):
        ret = []
        data = self.getColors()
        for side in data:
            new_side = []
            for color in side:
                new_color = self.rgb2hex(color[0], color[1], color[2])
                new_side.append(new_color)
            ret.append(new_side)
        return ret
    def rgb2hex(self, r, g, b):
        return '%02x%02x%02x' % (r, g, b)
    def normalizeSides(self, colors):
        data = []
        """ bottom side """
        for i in range(len(colors[2])-1, -1, -1):
            data.append(colors[2][i])
        """ bottom side """
        """ left side """
        for i in range(len(colors[3])-1, -1, -1):
            data.append(colors[3][i])
        """ left side """
        """ top side """
        for i in range(len(colors[0])):
            data.append(colors[0][i])
        """ top side """
        """ right side """
        for i in range(len(colors[1])):
            data.append(colors[1][i])
        """ right side """

        return data