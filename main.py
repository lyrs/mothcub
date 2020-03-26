#!/usr/bin/env python3

import cv2
import numpy as np


def find_letters_in(image):

  # binarization
  img_cp = image*1
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  ret, blwh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

  # finding connected compontents
  num_of_comps, comps, stats, _ = cv2.connectedComponentsWithStats(blwh, 4, cv2.CV_32S)

  for i in range(0, num_of_comps):
    x, y, a, b, s = stats[i][:]  # just like in school maths, coords & sides
    # i chose these values basing on my quick empirical research
    if (450 > a*b > 40) and (s < 0.80*a*b):
      cv2.rectangle(img_cp, (x,y), (x+a,y+b), (0,255,0), 5)

  return(img_cp)

def find_text_passage(image):
  
  letters = find_letters_in(image)
  # finding text passages
  mask = np.zeros((image.shape[:2]), np.uint8)
  for y in range(0, image.shape[0]):
    for x in range(0, image.shape[1]):
      if (letters[y][x] == [0, 255, 0]).all():
        mask[y][x] = 255

  # finding connected compontents again as i have no better idea
  num_of_comps, comps, stats, _ = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)

  for i in range(1, num_of_comps):
    x, y, a, b, s = stats[i][:]
    if a > b*1.2:
      cv2.rectangle(image, (x,y), (x+a,y+b), (255,0,0), 1)

  return(image)


drawing = cv2.imread('art/test/4')
derp = find_text_passage(drawing)

cv2.imshow("text passage?", derp)
cv2.waitKey(0)
