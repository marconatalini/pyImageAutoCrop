

'''
Created on 30 ago 2019

@author: marco
'''

from PIL import Image
import os

JPG_SOURCE_PATH = r's:\Disegni_listini\Europrofili'
JPG_SOURCE_PATH = r'c:\Users\Marco\symfony4\eurolist\public\jpgs'
JPG_DESTINATION_PATH = r'c:\Users\marco\Documents\Stampe\jpgs'

def isPortrait(size):
    if float(size[1]) / float(size[0]) > 2.0:
        return True
    else:
        return False
    
def isWhite(pixel):
    if pixel == (255,255,255):
        return True
    else:
        return False
    
def getBoundBox(im): #image object    
    left,upper,right,lower = im.size[0],im.size[1],0,0
    px = im.load()
    for x in range(im.size[0]):
        for y in range(im.size[1]):
            if not(isWhite(px[x,y])):
                if x < left:  left = x
                if y < upper: upper = y
                if x > right: right = x
                if y > lower: lower = y
    box = (left,upper,right,lower) #left,upper,right,lower
    return box

def autoCrop():    
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
    imfile = r"c:\Users\Marco\symfony4\eurolist\public\jpgs\16000720.jpg"
    im = Image.open(imfile)
    b = getBoundBox(im)
    im_crop = im.crop(b)
    im_crop.save(os.path.join(JPG_DESTINATION_PATH, 'prova.jpg'))
    im