#!/usr/bin/env python
import freenect
import cv
import numpy as np

cv.NamedWindow('depth')
running = True

def pretty_depth(depth):
  np.clip(depth, 0, 2**10 - 1, depth)
  depth >>= 2
  depth = depth.astype(np.uint8)
  return depth

def pretty_depth_cv(depth):
  import cv
  depth = pretty_depth(depth)
  image = cv.CreateImageHeader((depth.shape[1], depth.shape[0]),
                               cv.IPL_DEPTH_8U,
                               1)
  cv.SetData(image, depth.tostring(),
             depth.dtype.itemsize * depth.shape[1])
  return image

def display_depth(dev, data, timestamp):
  global running
  cv.ShowImage('Depth', pretty_depth_cv(data))
  if cv.WaitKey(10) == 27:
    running = False

def body(*args):
  if not running:
    raise freenect.Kill

print('end with ESC key')
freenect.runloop(depth=display_depth, body=body)
