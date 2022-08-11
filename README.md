# gst-opencv
Gstreamer OpenCV integration using Python

## OpenCV Python examples

### Open Image, Crop it and overlay text. Open Video and overlay text
```
python3 opencv_basics.py
```

### Open webcam directly from OpenCV
```
python3 opencv_webcam.py
```

### Open webcam from OpenCV using GStreamer
*NOTE*: The below command only works without venv on Ubuntu 22.04
```
python3 opencv_webcam.py
```

### Webcam v4l2 to cv2 to h264 encoded rtsp stream
*NOTE*: The below command only works without venv on Ubuntu 22.04

#### To Run Server
```
python3 v4l2_apsnk_apsrc_rtsp.py
```
#### To Run Gst Client
```
gst-launch-1.0 rtspsrc location=rtsp://127.0.0.1:8554/feed is-live=true ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! videoscale ! autovideosink
```
#### RTSP Uri To View on a video player like VLC
```
rtsp://127.0.0.1:8554/feed
```
