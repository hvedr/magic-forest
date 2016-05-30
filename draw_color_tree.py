# -*- coding: utf-8 -*-
"""
Created on Sun Apr 05 22:58:08 2015

@author: Konstantin Osminin
"""
import numpy as np
from PIL import Image, ImageDraw
import os

#Constants
new_br = 10 # Average new branches to grow on a branch
ang_std = 0.4

def branch(draw, x0,y0,length = 100, angle = np.pi/2,c = 100,depth = 1):
    ''' Draw a branch on a draw from (x0,y0) point with angle and length. 
        New branches will evolve with randomly with new_br average.'''
    if length > 0:    
        draw.line((x0,y0,x0 + length * np.cos(angle),y0 + length * np.sin(angle)),width = max(1,int(length/70)),fill = c)
    res_l = length
    while res_l > 5:
        #l = np.random.exponential(1./br) * res_l
        l = np.exp(np.random.randn() * 0.2 +np.log(0.3)) * res_l
        if (l < res_l) & (l > 10):
            ang = angle + (np.random.choice([-1,1]) + np.random.randn()) * ang_std
            x0,y0 = x0 + l * np.cos(angle),y0 + l * np.sin(angle)
            branch(draw, x0, y0, res_l - l,ang,c,depth=depth+1)
        res_l = res_l - l

def symm_branch(draw, x0,y0,length = 100, angle = np.pi/2,trunk_color = np.random.rand(3)*255, leaf_color = np.random.rand(3)*255,depth = 1):
    ''' Draw a branch on a draw from (x0,y0) point with angle and length. 
        New branches will evolve with randomly with new_br average.'''
    if length > 0:    
        draw.line(
           (x0,y0,x0 + length * np.cos(angle),y0 + length * np.sin(angle)),
           width = max(1,int(length/50)),
           fill = tuple([int(e) for e in trunk_color])
        )
    res_l = length
    while res_l > max(6,sum(draw.im.size)*0.003):
        #l = np.random.exponential(1./br) * res_l
        l = np.exp(np.random.randn(2) * 0.2 +np.log(0.33)) * res_l
        if (max(l) < res_l) & (min(l) > max(6,sum(draw.im.size)*0.003)):
            ang = angle + (np.random.permutation([-1,1]) + np.random.randn(2)) * ang_std
            c_new = leaf_color * 0.2 + trunk_color * 0.8
            #c_new = c * 1.1
            symm_branch(draw,  x0 + l[0] * np.cos(angle),y0 + l[0] * np.sin(angle), 1.05 * (res_l - l[0]),ang[0],trunk_color = c_new, leaf_color = leaf_color,depth=depth+1)
            symm_branch(draw,  x0 + l[1] * np.cos(angle),y0 + l[1] * np.sin(angle), 1.05 * (res_l - l[1]),ang[1],trunk_color = c_new, leaf_color = leaf_color,depth=depth+1)
            x0,y0 = x0 + max(l) * np.cos(angle),y0 + max(l) * np.sin(angle)
        res_l = res_l - max(l)
#        print(str(depth)+' '+str(res_l))

#Main
x_size = 2*500
y_size = 4*500
im = Image.new('RGBA', (x_size, y_size))  
draw = ImageDraw.Draw(im) 
trunk_color = np.array([50,20,0])
leaf_color = np.array([255,255,250])


#draw a forest
trees_number = 60
for (x,y) in sorted(np.random.rand(trees_number,2),key = lambda l:l[1]):
    x,y = int(x_size * (x * 0.72 + 0.12)), int((y+0.2) * y_size * 0.84 )
    tcol = trunk_color + np.random.randn(3) * 100
    #tcol = tcol - min(tcol) + + np.random.randn(3) * 20
    lcol = leaf_color  + np.random.randn(3) * 250
    lcol = lcol - min(lcol) + + np.random.randn(3) * 10
    symm_branch(draw,x,y,np.random.randn() * int(x_size * 0.1) + int(y_size * 0.1),-np.pi/2 + np.random.randn() * ang_std/8, trunk_color = tcol, leaf_color = lcol)

#One tree
#symm_branch(draw,x_size / 2,int(y_size * 0.98),int(y_size * 0.9),-np.pi/2,trunk_color, leaf_color,depth=1) #draw a tree
#symm_branch(draw,x_size / 2,int(y_size * 0.98),int(y_size * 0.86),-np.pi/2,np.array([0,10,0]), np.array([250,2,45]),depth=1) #draw a tree

im.save('forest' + str(len(os.listdir('.'))) + '.png',format = 'png',quality = 90)
im.show()
