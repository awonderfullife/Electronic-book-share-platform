from PIL import Image
import sys
import numpy as np
import os


for level in range(0,4):

    script_dir = os.path.dirname(__file__)
    im = Image.open(os.path.join(script_dir,'img',str(level),'0','0.png'))
    width = im.size[0]
    total_width = width*(2**level)
    new_im = Image.new('RGB',(total_width,total_width))
    for i in range(0,2**level):
        for j in range(0, 2 ** level):
            image = Image.open(os.path.join(script_dir,'img',str(level),str(i),
                                            str(j)+'.png'))
            new_im.paste(image,(i*width,j*width))

    new_im.save(os.path.join(script_dir,str(level)+'_result.png'))




