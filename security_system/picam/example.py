from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput
import time

p2 = Picamera2()

#Image
# camera_config = p2.create_preview_configuration()
# p2.configure(camera_config)
# p2.start_preview(Preview.QTGL)
# p2.start()
# time.sleep(5)
# p2.capture_file("exampe.jpg")

#Video
# video_config = p2.create_video_configuration()
# p2.configure(video_config)
# 
# encoder = H264Encoder(bitrate=10000000)
# output = "test.h264"
# 
# p2.start_recording(encoder, output)
# time.sleep(10)
# p2.stop_recording()

#CircualVideo
p2.configure(p2.create_video_configuration())
encoder = H264Encoder()
output = CircularOutput()
p2.start_recording(encoder, output)

output.fileoutput = "circular.h264"
output.start()

