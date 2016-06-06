import os

import numpy as np
from PIL import Image, ImageDraw

#AVERAGE_BRANCHES = 10
ANGLE_STD = 0.4

#TRUNC_COLOR = [50, 20, 0]
#LEAF_COLOR = [255, 255, 250]


class TreeImage(object):

    def __init__(self, count = 80, width = 500, height = 300, trunk_color = (110,90,70),leaf_color = (130,230,50),background_color = (100, 205, 150, 0), color_std = 1):
        self.image = Image.new('RGBA', (width, height),background_color)
        self.width = width
        self.height = height
        self.draw = ImageDraw.Draw(self.image)
        self.color = {
            'trunk':  np.array(trunk_color),
            'leaf': np.array(leaf_color)
        }
        self.trees_count = count
        self.color_std = color_std

    def branch(self, x0, y0, length=100, angle=np.pi / 2, c=100, depth=1):
        ''' Draw a branch on a draw from (x0,y0) point with angle and length.
        New branches will evolve with randomly with new_br average.'''
        if length > 0:
            self.draw.line(
                (x0, y0, x0 + length * np.cos(angle), y0 + length * np.sin(angle)),
                width=max(1, int(length / 70)),
                fill=c
            )
            res_l = length

        while res_l > 5:
            #l = np.random.exponential(1./br) * res_l
            l = np.exp(np.random.randn() * 0.2 + np.log(0.3)) * res_l
            if (l < res_l) & (l > 10):
                ang = angle + \
                    (np.random.choice([-1, 1]) +
                     np.random.randn()) * ANGLE_STD
                x0, y0 = x0 + l * np.cos(angle), y0 + l * np.sin(angle)
                self.branch(x0, y0, res_l - l, ang, c, depth=depth + 1)
                res_l = res_l - l

    def symm_branch(self, x0, y0, length=100, angle=np.pi / 2, trunk_color=np.random.rand(3) * 255, leaf_color=np.random.rand(3) * 255, depth=1):
        ''' Draw a branch on a draw from (x0,y0) point with angle and length.
        New branches will evolve with randomly with new_br average.'''
        if length > 0:
            self.draw.line(
                (x0, y0, x0 + length * np.cos(angle), y0 + length * np.sin(angle)),
                width=max(1, int(length / 50)),
                fill=tuple([int(e) for e in trunk_color])
            )
        res_l = length       
        while res_l > max(6, sum(self.draw.im.size) * 0.003):
            #l = np.random.exponential(1./br) * res_l
            l = np.exp(np.random.randn(2) * 0.2 + np.log(0.33)) * res_l
            if (max(l) < res_l) & (min(l) > max(6, sum(self.draw.im.size) * 0.003)):
                ang = angle + \
                    (np.random.permutation([-1, 1]) +
                     np.random.randn(2)) * ANGLE_STD
                c_new = leaf_color * 0.2 + trunk_color * 0.8
                #c_new = c * 1.1
                self.symm_branch(
                    x0 + l[0] * np.cos(angle),
                    y0 + l[0] * np.sin(angle),
                    1.05 * (res_l - l[0]),
                    ang[0],
                    trunk_color=c_new,
                    leaf_color=leaf_color,
                    depth=depth + 1
                )
                self.symm_branch(
                    x0 + l[1] * np.cos(angle),
                    y0 + l[1] * np.sin(angle),
                    1.05 * (
                        res_l - l[1]),
                    ang[1],
                    trunk_color=c_new,
                    leaf_color=leaf_color,
                    depth=depth + 1
                )
                x0, y0 = x0 + max(l) * np.cos(angle), y0 + \
                    max(l) * np.sin(angle)
            res_l = res_l - max(l)

    def create(self):
        # old name - create. 
        # draw a forest
        for (x, y) in sorted(np.random.rand(self.trees_count, 2), key=lambda l: l[1]):
            tree_length = -1
            while tree_length < 0:
                tree_length = (1 + np.random.randn()) / 2 * (int(self.width * (1./self.trees_count)**0.5) + int(self.height  * (1./self.trees_count)**0.5))
            x1 = int(tree_length / 3. + x * (self.width - 2./3 * tree_length))
            y1 = int( tree_length + y * (self.height - tree_length))
            tcol = self.color['trunk'] + np.random.randn(3) * 100 * self.color_std
            lcol = self.color['leaf'] + np.random.randn(3) * 250 * self.color_std
            lcol = lcol - min(lcol) + np.random.randn(3) * 10

            self.symm_branch(
                x1,
                y1,
                tree_length,
                -np.pi / 2 + np.random.randn() * ANGLE_STD / 8,
                trunk_color=tcol,
                leaf_color=lcol
            )
        return self.image 
