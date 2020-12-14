from pytesseract import*
import argparse 
import cv2 

ap = argparse.ArgumentParser() 

ap.add_argument("-i", "--image", 
        required=True, dest="image",
        help="path to input image to be OCR'd") 
ap.add_argument("-c", "--min-conf", 
        type=int, default=0, dest="min_conf",
        help="mininum confidence value to filter weak text detection") 
args = ap.parse_args() 

# load and convert
images = cv2.imread(args.image) 
rgb = cv2.cvtColor(images, cv2.COLOR_BGR2RGB) 
results = pytesseract.image_to_data(rgb, output_type=Output.DICT)

# loop over findings
for i in range(0, len(results["text"])):   
  
  # bounding box
  x = results["left"][i] 
  y = results["top"][i] 
  w = results["width"][i] 
  h = results["height"][i] 

  # text and confidence
  text = results["text"][i] 
  conf = int(results["conf"][i]) 
  
  # filter out 
  if conf > args.min_conf: 
    
    text = "".join(text).strip() 
    cv2.rectangle(images, 
          (x, y), 
          (x + w, y + h), 
          (17, 163, 252), 1) 
    cv2.putText(images, 
          text, 
          (x, y - 5), 
          cv2.FONT_HERSHEY_SIMPLEX, 
          0.5, (200, 0, 150), 1) 
    
cv2.imshow("Result", images) 
cv2.waitKey(0) 
