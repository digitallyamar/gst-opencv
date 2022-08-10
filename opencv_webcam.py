import cv2

fps = 15
frame_width = 640
frame_height = 480

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
cap.set(cv2.CAP_PROP_FPS, fps)

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