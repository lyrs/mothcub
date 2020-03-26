#!/usr/bin/env python3

import cv2
import numpy as np


def find_letters_in(image):

  # binarization
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  ret, blwh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

  # finding connected compontents
  num_of_comps, comps, stats, _ = cv2.connectedComponentsWithStats(blwh, 4, cv2.CV_32S)

  for i in range(0, num_of_comps):
    x, y, a, b, s = stats[i][:]  # just like in school maths, coords & sides
    # i chose these values basing on my quick empirical research
    if 450 > a*b > 40:
      cv2.rectangle(image, (x,y), (x+a,y+b), (0,255,0), 2)


drawing = cv2.imread('art/test/2')
find_letters_in(drawing)

cv2.imshow("letters?", drawing)
cv2.waitKey(0)
