#!/usr/bin/env python3

import cv2
import numpy as np
import sys
import os
import pytesseract
from tqdm import tqdm

def normalize(s):
  return " ".join(s.lower().split())

def contains(i, j):
    x1, y1, w1, h1, _ = i
    x2, y2, w2, h2, _ = j
    X1 = x1 + w1; Y1 = y1 + h1
    X2 = x2 + w2; Y2 = y2 + h2
    return (x1 <= x2 and y1 <= y2) and (X2 <= X1 and Y2 <= Y1)


def find_letters_in(image):

  # binarization
  img_cp = image*1
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  ret, blwh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

  # finding connected compontents
  comps, labels, stats, cents = cv2.connectedComponentsWithStats(blwh, 4, cv2.CV_32S)

  # check which bbs contains other
  # background always contains others
  badccs = [0]
  for i in range(1, comps):
    for j in range(1, comps):
      if contains(stats[i][:], stats[j][:]) and i != j:
        badccs.append(i)
        break

  # remove definetly non-text ccs
  for cc_label in badccs:
    (labels[labels == cc_label]) = 0
  #stats = np.delete(stats, badccs, axis=0)

  # check which are surronded by other letter candidates
  goodccs = []
  for c in range(1, comps):
    if c not in badccs:
      surr = False
      x,y,a,b,s = stats[c][:]
      # check neighobring bbs
      #if a*b*0.75 < s:
      #  surr = True
      for cor in [(x,y-b),(x+a,y),(x,y+b),(x-a,y)]:
        bb = labels[cor[1]:cor[1]+b, cor[0]:cor[0]+a]
        # if are not empty
        if bb.any():
          for u in np.unique(bb[bb > 0]):
            if abs(stats[u][3] - b) < 0.5*b:
              surr = True
              goodccs.append(u)
      if surr:
        goodccs.append(c)

  # remove the single ones
  #_, indic = np.unique(goodccs, return_index=True)
  #goodccs = np.delete(goodccs, indic)

  for c in set(goodccs):
    x,y,a,b,_ = stats[c][:]
    cv2.rectangle(img_cp, (x,y), (x+a,y+b), (255,0,0), 1)

  #cv2.imshow("?",img_cp)
  #cv2.waitKey()

  good_in = sorted(list(set(goodccs)))
  return(stats[good_in], cents[good_in])

def find_text_passage(image):
  
  letter_rois, cents = find_letters_in(image)
  letter_rois = np.vstack((np.zeros(5, np.uint8), letter_rois))
  cents = np.vstack((np.zeros(2), cents))
  # finding text passages
  mask = np.zeros((image.shape[:2]), dtype=np.uint8)
  for i,r in enumerate(letter_rois):
    if i > 0:
      x,y,a,b,_ = r
      mask[y:y+b, x:x+a] = i

  # find far left letter candidates and consume
  text_passages = []
  for i in range(1, letter_rois.shape[0]):
    x,y,a,b,_ = letter_rois[i][:]
    if not (mask[y:y+b, x-b:x].any()):
      tp = [i]
      while mask[y:y+b, x+a:x+a+b].any():
        ccnum = np.unique(mask[y:y+b, x+a:x+a+b])[-1]
        _, ry2 = cents[ccnum]
        if ry2 >= y and ry2 <= y+b:
          tp.append(ccnum)
          x,y,a,b,_ = letter_rois[ccnum][:]
        else:
          break
      text_passages.append(tp)
  
  final = []
  for tp in text_passages:
    x = letter_rois[tp[0],0]
    X = letter_rois[tp[-1],0] + letter_rois[tp[-1],2]
    rois = letter_rois[sorted(tp)][:]
    y = min(rois[:,1])
    Y = max(rois[:,1]+rois[:,3])
    final.append((x,y,X,Y))
    #cv2.rectangle(image, (x,y), (X,Y), (255,0,0), 1)
    #cv2.imshow('?', image)

  return(final)


def OCR(image):
  M = 5
  coords = find_text_passage(image)
  texts = []
  for cd in coords:
    x,y,X,Y = cd 
    #cv2.imshow(str(cd), image[y-M:Y+M,x-M:X+M])
    #cv2.waitKey()
    texts.append(pytesseract.image_to_string(
                    image[y-M:Y+M,x-M:X+M], lang='eng'))
  return " ".join(list(filter(None,texts)))


with open("results.txt",'w+') as res:
  for d in tqdm(sorted(os.listdir("testset/"))):
    drawing = cv2.imread("testset/"+d)
    #herp = find_letters_in(drawing)
    res.write(normalize(OCR(drawing)) + "\n")

#cv2.imshow("text passage?", derp)
#cv2.waitKey(0)
