import cv2
import numpy as np

print("Using Python OpenCV: " + cv2.__version__)

img = cv2.imread('road.jpg')

# Reading dimensions of an image
h, w = img.shape[:2]
print ('Height = {}, Width = {}'.format(h, w))

# Reading RGB value of a pixel
(B, G, R) = img[100, 100]
print('R = {}, G = {}, B = {}'.format(R, G, B))

# Here, the last element specifies the channel
# R = 2, G = 1, B = 0
nB = img[100, 100, 0]

print('nB = {}'.format(nB))

# Crop to a specific region
cropped_img = img[200:500, 200:700]
cv2.imshow("cropped", cropped_img)
# Press any key to contiue
print ('Press any key to contiue')
cv2.waitKey(0)

# Add text overlay to an image
ov_txt_img = cv2.putText(cropped_img, 'Hello!', (100, 150), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)
cv2.imshow("Text Overlay", ov_txt_img)
# Press any key to contiue
print ('Press any key to contiue')
cv2.waitKey(0)

# Read a video file frame by frame
cap = cv2.VideoCapture('skyscrapers.mp4')

if (cap.isOpened() == False):
    print("Error opening video file")

print ('Press Q key to quit')
while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        # Add text overlay on each frame
        ov_txt_frame = cv2.putText(frame, 'Good evening!', (100, 150), 
                   cv2.FONT_HERSHEY_SIMPLEX, 2, (128, 0, 255), 2)
        cv2.imshow('Frame', ov_txt_frame)

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        print ('Failed to read frame!')
        break

cap.release()
cv2.destroyAllWindows()