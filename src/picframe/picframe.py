#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2024-07-04T15:52:31-04:00

@author: nate
"""
import os
import numpy as np
import PIL.Image


def borderize(arr0, arr1):
    pass


def beframe(im0: PIL.Image.Image, **kwargs):
    """
    Apply a frame to an image
    """
    basedir = os.path.dirname(__file__)
    assets = os.path.join(basedir, "assets")

    builtin_images = []
    for img in os.listdir(assets):
        if not img.endswith('.png'):
            continue
        fpath = os.path.join(assets, img)
        builtin_images.append(fpath)

    builtin_images = sorted(builtin_images)

    params = {
        "frameid": 0,
        "mattesize": 0,
        "mattecolor": "cornsilk",
        "bordersize": 0,
        "bordercolor": "black",
        # Controls the css "border: ridge" effect
        "shade": 0,
        "adjust": "100,100,100",
        "opacity": 50,
        "distance": 1,
    }
    params.update(kwargs)
    frame_path = builtin_images[params['frameid']]
    frame = PIL.Image.open(frame_path)

    if frame.mode == "RGB":
        a_channel = PIL.Image.new('L', frame.size, 255)
        frame.putalpha(a_channel)

    w1 = im0.width
    h1 = im0.height

    w2 = frame.width
    h2 = frame.height

    # compute center section width and height
    w3 = w1 + (2 * params['bordersize']) + (2 * params['mattesize'])
    h3 = h1 + (2 * params['bordersize']) + (2 * params['mattesize'])

    # compute outfile image size
    w4 = w3 + (2 * w2)
    h4 = h3 + (2 * h2)

    output_arr = np.zeros((h3, w3, 4))

    off1 = params['bordersize'] + params['mattesize']
    off2 = params['bordersize'] + params['mattesize']
    output_arr[off1:off1+h1, off2:off2+w1, :] = np.array(im0)

    out_shape = (h4, w4, 4)
    output_arr = np.zeros(out_shape)

    btm_r = np.array(frame)
    btm_l = np.flip(btm_r, 1)
    top_l = np.flip(btm_l, 0)
    top_r = np.flip(top_l, 1)

    output_arr[w4-w2:, h4-h2:, :] = btm_r
    output_arr[0:w2, 0:h2, :] = top_l
    output_arr[w4-w2:, 0:h2, :] = btm_l
    output_arr[0:w2, h4-h2:, :] = top_r

    size1 = w4 - w2 - w2
    size2 = h4 - h2 - h2

    bottom = btm_r[:, 0, :]
    bottom = np.repeat(bottom[:, np.newaxis, :], size1, axis=1)

    side = btm_r[0, :, :]
    side = np.repeat(side[np.newaxis, :, :], size2, axis=0)

    # insert frame pixels
    output_arr[h4-h2:, w2:w4-w2, :] = bottom
    output_arr[0:h2, w2:w4-w2, :] = np.flip(bottom, 0)
    output_arr[h2:w4-h2, w4-w2:, :] = side
    output_arr[h2:h4-h2, 0:w2, :] = np.flip(side, 1)

    output_arr[h2:h4-h2, w2:w4-w2, :] = arr0

    out_image = PIL.Image.fromarray(output_arr.astype('uint8'), 'RGBA')
    out_image.show()
    breakpoint()
    #im1 = PIL.Image.fromarray(arr, mode='RGBA')
