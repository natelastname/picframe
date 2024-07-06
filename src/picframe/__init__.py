# -*- coding: utf-8 -*-
"""
Created on 2024-07-04T15:50:09-04:00

@author: nate
"""


import os
import sys
import argparse

import PIL.Image

from . import picframe


def get_builtin_frames():
    basedir = os.path.dirname(__file__)
    assets = os.path.join(basedir, "assets")
    builtin_images = []
    for img in os.listdir(assets):
        if not img.endswith('.png'):
            continue
        fpath = os.path.join(assets, img)
        builtin_images.append(fpath)

    builtin_images = sorted(builtin_images)
    return builtin_images

def beframe():
    parser = argparse.ArgumentParser(
        prog="picframe",
        description="Apply a decorative frame to an image."
    )

    parser.add_argument(
        "infile",
        help="Input image.",
        type=argparse.FileType("r")
    )

    parser.add_argument(
        "outfile",
        help="Output image",
        type=str
    )

    parser.add_argument(
        "--frameimg",
        help="Image to use as a frame",
        type=argparse.FileType("r")
    )

    parser.add_argument(
        "--frameid",
        help="Use a builtin image as a frame",
        default=None,
        type=str
    )


    parser.add_argument(
        "--mattesize",
        help="Size of the mat",
        default=24,
        type=int
    )

    parser.add_argument(
        "--mattecolor",
        help="Color of the mat",
        default="cornsilk",
        type=str
    )


    parser.add_argument(
        "--bordersize",
        help="Size of the border",
        default=3,
        type=int
    )

    parser.add_argument(
        "--bordercolor",
        help="Color of the border",
        default="black",
        type=str
    )

    parser.add_argument(
        "--dropshadow_opacity",
        help="Opacity of the dropshadow",
        default=1.0,
        type=float
    )

    parser.add_argument(
        "--dropshadow_opacity",
        help="Radius of gaussian blur",
        default=6.0,
        type=float
    )

    parser.add_argument(
        "--dropshadow_offset_x",
        help="x offset of the dropshadow",
        default=0,
        type=int
    )

    parser.add_argument(
        "--dropshadow_offset_y",
        help="y offset of the dropshadow",
        default=0,
        type=int
    )

    args = parser.parse_args()

    infile = str(args.infile.name)
    outfile = str(args.outfile)

    frame = None

    if not args.frameimg and not args.frameid:
        # Assume frameid = 0
        img_paths = get_builtin_frames()
        frame_path = img_paths[0]
        frame = PIL.Image.open(frame_path)
    elif args.frameimg and args.frameid:
        print("Error: Cannot specify both FRAMEID and FRAMEIMG.")
        parser.print_usage()
        sys.exit(1)
    elif args.frameimg:
        frame_path = str(args.frameimg.name)
        frame = PIL.Image.open(frame_path)
    if args.frameid:
        img_paths = get_builtin_frames()
        frame_path = img_paths[int(args.frameid)]
        frame = PIL.Image.open(frame_path)

    im0 = PIL.Image.open(args.infile.name)

    im1 = picframe.beframe(
        im0,
        frame,
        mattesize=args.mattesize,
        mattecolor=args.mattecolor,
        bordersize=args.bordersize,
        bordercolor=args.bordercolor,
        dropshadow_opacity=args.dropshadow_opacity,
        dropshadow_blur_radius=args.dropshadow_blur_radius,
        dropshadow_offset_x=args.dropshadow_offset_x,
        dropshadow_offset_y=args.dropshadow_offset_y
    )

    im1.save(outfile)
