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
    if ret == False:
        break

    # Add text overlay on each frame
    ov_txt_frame = cv2.putText(frame, 'Press Q to exit!', (100, 350),
                cv2.FONT_HERSHEY_SIMPLEX, 2 , (128, 0, 255), 2)

    out.write(ov_txt_frame)
    if show:
        cv2.imshow("gst_cv2_webcam_stream", ov_txt_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break