#!/usr/bin/env python3

# Gstreamer client command to consume feed;
# gst-launch-1.0 rtspsrc location=rtsp://127.0.0.1:8554/feed is-live=true 
# ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! videoscale ! autovideosink

# RTSP url to view on a video player
# rtsp://127.0.0.1:8554/feed

import cv2
import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GObject, GstRtspServer

class CamFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, **properties):
        super(CamFactory, self).__init__(**properties)
        self.cap = cv2.VideoCapture(0)
        self.num_frames = 0
        self.fps = 30
        self.duration = 1 / self.fps * Gst.SECOND # duration of a frame in nanoseconds
        self.launch_string = 'appsrc name=source is-live=true block=true format=GST_FORMAT_TIME ' \
                             'caps=video/x-raw,format=BGR,width=640,height=480,framerate={}/1 ' \
                             '! videoconvert ! video/x-raw,format=I420 ' \
                             '! clockoverlay ' \
                             '! x264enc speed-preset=ultrafast tune=zerolatency ' \
                             '! rtph264pay config-interval=1 name=pay0 pt=96'.format(self.fps)

    def on_need_data(self, src, length):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
            # Add text overlay on each frame
                ov_txt_frame = cv2.putText(frame, '[LIVE]', (30, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)                
                data = ov_txt_frame.tostring()
                buf = Gst.Buffer.new_allocate(None, len(data), None)
                buf.fill(0, data)
                buf.duration = self.duration
                timestamp = self.num_frames * self.duration
                buf.pts = buf.dts = int(timestamp)
                buf.offset = timestamp
                self.num_frames += 1
                ret_val = src.emit('push-buffer', buf)
                print('pushed buffer, frame {}, duration {} ns, durations {} s'.format(self.num_frames,
                                                                                       self.duration,
                                                                                       self.duration / Gst.SECOND))
                if ret_val != Gst.FlowReturn.OK:
                    print(ret_val)
    
    def do_create_element(self, url):
        return Gst.parse_launch(self.launch_string)
    
    def do_configure(self, rtsp_media):
        self.num_frames = 0
        appsrc = rtsp_media.get_element().get_child_by_name('source')
        appsrc.connect('need-data', self.on_need_data)


class GstServer(GstRtspServer.RTSPServer):
    def __init__(self, **properties):
        super(GstServer, self).__init__(**properties)
        self.factory = CamFactory()
        self.factory.set_shared(True)
        self.get_mount_points().add_factory("/feed", self.factory)
        self.attach(None)

GObject.threads_init()
Gst.init(None)

server = GstServer()

loop = GObject.MainLoop()
loop.run()