#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2024-07-04T10:14:14-04:00

@author: nate
"""
import PIL.Image
import numpy as np

import picframe
import importlib.resources


im0 = PIL.Image.open("/home/nate/test2.png")
im1 = picframe.picframe.beframe(im0, mattesize=32)
#im1 = picframe.picframe.beframe(im0, mattesize=0, bordersize=0)

im1.show()

breakpoint()
