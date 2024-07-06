#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2024-07-04T15:52:31-04:00

@author: nate
"""
import os
import numpy as np
import PIL.Image
import PIL.ImageFilter
import PIL.ImageDraw


def borderize(arr0, arr1, separate=False):

    if arr1.size == 0:
        return arr0

    w1 = arr0.shape[1]
    h1 = arr0.shape[0]
    w2 = arr1.shape[1]
    h2 = arr1.shape[0]

    # compute outfile image size
    w4 = w1 + (2 * w2)
    h4 = h1 + (2 * h2)

    out_shape = (h4, w4, 4)
    output_arr = np.zeros(out_shape)

    btm_r = arr1
    btm_l = np.flip(btm_r, 1)
    top_l = np.flip(btm_l, 0)
    top_r = np.flip(top_l, 1)

    output_arr[h4-h2:, w4-w2:, :] = btm_r
    output_arr[0:h2, 0:w2, :] = top_l
    output_arr[h4-h2:, 0:w2, :] = btm_l
    output_arr[0:h2, w4-w2:, :] = top_r

    size1 = w4 - w2 - w2
    size2 = h4 - h2 - h2

    bottom = btm_r[:, 0, :]
    bottom = np.repeat(bottom[:, np.newaxis, :], size1, axis=1)

    side = btm_r[0, :, :]
    side = np.repeat(side[np.newaxis, :, :], size2, axis=0)

    # insert left/right/up/down frame pixels
    output_arr[h4-h2:, w2:w4-w2, :] = bottom
    output_arr[0:h2, w2:w4-w2, :] = np.flip(bottom, 0)
    output_arr[h2:h4-h2, w4-w2:, :] = side
    output_arr[h2:h4-h2, 0:w2, :] = np.flip(side, 1)

    outer = output_arr

    inner = np.zeros(output_arr.shape)
    inner[h2:h4-h2, w2:w4-w2, :] = arr0

    if separate:
        return (outer, inner)

    return outer + inner


def add_alpha(im0: PIL.Image.Image):
    if im0.mode == "RGB":
        a_channel = PIL.Image.new('L', im0.size, 255)
        im0.putalpha(a_channel)
    return im0


def multiply_achannel(im0: PIL.Image.Image, mult: float):
    arr0 = np.array(im0)
    arr0[:, :, 3] = arr0[:, :, 3] * mult
    arr0 = arr0.astype('uint8')
    return PIL.Image.fromarray(arr0, 'RGBA')


def beframe(im0: PIL.Image.Image, frame: PIL.Image.Image, **kwargs):
    """
    Apply a frame to an image
    """
    params = {
        "frameid": 0,
        "mattesize": 32,
        "mattecolor": "cornsilk",
        "bordersize": 2,
        "bordercolor": "black",
        # Controls positioning and intensity of the dropshadow of the
        # frame on the mat.
        "dropshadow_opacity": 0.5,
        "dropshadow_blur_radius": 6,
        "dropshadow_offset_x": 0,
        "dropshadow_offset_y": 0
    }
    params.update(kwargs)

    bordersize = int(params['bordersize'])
    bordercolor = PIL.ImageColor.getrgb(str(params["bordercolor"]))
    arr_border = np.full(
        (bordersize, bordersize, 4),
        bordercolor + (255,),
        dtype=np.uint8
    )

    mattesize = int(params['mattesize'])
    mattecolor = PIL.ImageColor.getrgb(str(params["mattecolor"]))
    arr_matte = np.full(
        (mattesize, mattesize, 4),
        mattecolor + (255,),
        dtype=np.uint8
    )

    arr0 = np.array(add_alpha(im0))
    arr_frame = np.array(add_alpha(frame))
    # add the border
    out0 = borderize(arr0, arr_border)
    # add the matte
    out0 = borderize(out0, arr_matte)
    # Create the frame
    (outer, inner) = borderize(out0, arr_frame, separate=True)

    black = np.zeros(arr_frame.shape)
    black[:, :, 3] = 255
    # Create the shadow by borderizing with a dummy image (a black square)
    (shadow, _) = borderize(out0, black, separate=True)

    outer = PIL.Image.fromarray(outer.astype('uint8'), 'RGBA')
    inner = PIL.Image.fromarray(inner.astype('uint8'), 'RGBA')

    shadow = PIL.Image.fromarray(shadow.astype('uint8'), 'RGBA')

    radius = params["dropshadow_blur_radius"]
    shadow = shadow.filter(PIL.ImageFilter.GaussianBlur(radius=radius))

    shadow = multiply_achannel(shadow, params['dropshadow_opacity'])

    shadow_offset = PIL.Image.new('RGBA', outer.size)
    off_x = params['dropshadow_offset_x']
    off_y = params['dropshadow_offset_y']
    shadow_offset.paste(shadow, box=[off_x, off_y])

    # combine the shadow and the frame
    with_shadow = PIL.Image.alpha_composite(shadow_offset, outer)

    #with_shadow = PIL.Image.composite(outer, shadow_offset, outer)
    # combine the shadow/frame and the inner portion
    result = PIL.Image.alpha_composite(inner, with_shadow)
    #result = with_shadow
    return result
