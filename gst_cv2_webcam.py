import cv2

fps = 15
frame_width = 640
frame_height = 480
show = True

webcam_app_sink = "v4l2src device=/dev/video0 ! videoconvert ! appsink"
appsink2file = "appsrc ! videoconvert ! x264enc ! video/x-h264, profile=baseline ! matroskamux ! filesink location=webcam_stream.mkv"


cap = cv2.VideoCapture(webcam_app_sink, cv2.CAP_GSTREAMER)


# Create videowriter
out = cv2.VideoWriter(appsink2file, 0, fps, (frame_width, frame_height), True)

if not cap.isOpened():
    print("Cannot capture from camera. Exiting.")
    quit()

if not out:
    print("Cannot write. Exiting.")
    quit()

while True:
    ret, frame = cap.read()
    #
    if ret == False:
        break

    out.write(frame)
    if show:
        cv2.imshow("webcam_stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break