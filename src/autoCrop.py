

'''
Created on 30 ago 2019

@author: marco
'''

from PIL import Image
import os
from builtins import input

JPG_SOURCE_PATH = r's:\Disegni_listini\Europrofili'
#JPG_SOURCE_PATH = r'c:\Users\Marco\symfony4\eurolist\public\jpgs'
JPG_DESTINATION_PATH = r'c:\Users\marco\Documents\Stampe\jpgs'

def isPortrait(size):
    if float(size[1]) / float(size[0]) > 2.0:
        return True
    else:
        return False
    
def isWhite(pixel):
    if type(pixel) == tuple and pixel == (255,255,255):
        return True
    elif pixel >= 220:
        return True
    else:
        return False
    
def addAlpha(image, limit = 255):
    img = image.convert("RGBA")
    
    pixdata = img.load()
    
    width, height = image.size
    for y in range(height):
        for x in range(width):
            #print(pixdata[x, y])
            i = pixdata[x, y]
            if i[0] >= limit and i[1] >= limit and i[2] >= limit and i[3] >= limit:  
                pixdata[x, y] = (255, 255, 255, 0)    
    return img
    
def getBoundBox(image, border = 0): #image object
    left,upper,right,lower = image.size[0]-border,image.size[1]-border,0,0
    px = image.load()
    for x in range(border, image.size[0]-border):
        for y in range(border, image.size[1]-border):
            if not(isWhite(px[x,y])):
                if x < left:  left = x
                if y < upper: upper = y
                if x > right: right = x
                if y > lower: lower = y
                #input("{} : {} {} {} {}".format(px[x,y],left,upper,right,lower))
    box = (left+2,upper+2,right+2,lower+2) #left,upper,right,lower
    return box

def landscapeIt(image):
    if isPortrait(image.size):
        return image.rotate(-90, expand=True)
    
def autoCrop(image):
    b = getBoundBox(image)
    return image.crop(b)

def test():    
    with os.scandir(JPG_SOURCE_PATH) as jpgs:
        for entry in jpgs:
            if not entry.name.startswith('.') and entry.is_file() and entry.name.endswith('jpg'):
                im = Image.open(os.path.join(JPG_SOURCE_PATH, entry.name))
                print(im.format, im.size, im.mode, entry.name)
                if isPortrait(im.size):
#                     im.rotate(-90, expand=True).show()
                    im2 = im.rotate(-90, expand=True)
                    im2.save(os.path.join(JPG_DESTINATION_PATH, entry.name))
                    
#                     if input('Giro e salvo? Y/n').upper() == 'Y':
#                         im2 = im.rotate(-90, expand=True)
#                         im2.save(os.path.join(JPG_DESTINATION_PATH, entry.name))

if __name__ == '__main__':
    imfile = r"c:\Users\marco\Documents\Stampe\jpg300\C.535.12.jpg"
    im = Image.open(imfile)
    b = getBoundBox(im,10)
    print(im.size, b)
    im_crop = im.crop(b)
    im_alpha = addAlpha(im_crop, 200)
    
    im_alpha.save(os.path.join(JPG_DESTINATION_PATH, 'prova.png'), "PNG")
    
    