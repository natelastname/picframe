#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2024-07-04T10:14:14-04:00

@author: nate
"""
import os
import PIL.Image
import picframe

basedir = os.path.dirname(__file__)
demo_imgs = os.path.join(basedir, "demo_imgs")
frames = picframe.get_builtin_frames()

######################################################################
# Image 1: coolguy1.png
######################################################################
path = os.path.join(demo_imgs, "coolguy1.png")
img = PIL.Image.open(path)
frame = PIL.Image.open(frames[0])
framed = picframe.picframe.beframe(img, frame)
outfile = os.path.join(demo_imgs, "coolguy1-framed.png")
framed.save(outfile)

######################################################################
# Image 2: coolguy1.png
######################################################################
path = os.path.join(demo_imgs, "pom.png")
img = PIL.Image.open(path)
frame = PIL.Image.open(frames[3])
framed = picframe.picframe.beframe(img, frame)
outfile = os.path.join(demo_imgs, "pom-framed.png")
framed.save(outfile)

######################################################################
# Image 3: test.png
######################################################################
path = os.path.join(demo_imgs, "test.png")
img = PIL.Image.open(path)
framed = picframe.picframe.beframe(
    img,
    img,
    mattesize=0,
    mattecolor="purple",
    bordersize=0,
    bordercolor="green",
    dropshadow_opacity=0.9,
    dropshadow_blur_radius=6,
    dropshadow_offset_x=-10,
    dropshadow_offset_y=0
)
outfile = os.path.join(demo_imgs, "test-framed.png")
framed.save(outfile)
