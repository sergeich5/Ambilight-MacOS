import config as configuration
import ScreenPixel as SP
import Arduino as AR
import json
import requests
from time import sleep

if __name__ == '__main__':
    m = 254
    
    conf = configuration.config()
    
    sp = SP.ScreenPixel(
        top = conf.top,
        right = conf.right,
        bottom = conf.bottom,
        left = conf.left,
        
        height = conf.height,
        width = conf.width,
        
        offsetTop = conf.offsetTop,
        offsetRight = conf.offsetRight,
        offsetBottom = conf.offsetBottom,
        offsetLeft = conf.offsetLeft,
        
        step = conf.step
    )
    ar = AR.Arduino()
    
    old_data = ''
    while 1:
        brightness = 100
        """max(sp.getBrightness(), 44)"""
        data = sp.getColors()
        
        colors = sp.normalizeSides(data)
        
        data = chr(255) + chr(min(m, brightness))
        
        """data += chr(max(1, sp.getBrightness()))"""
        for color in colors:
            for channel in color:
                data += chr(min(m, channel))
        """data += chr(max(m, color[0])) + chr(max(m, color[1])) + chr(max(m, color[2]))"""
            
        if not old_data==data:
            ar.sendPacket(data)
        old_data = data
        sleep(0.05)