from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput, FfmpegOutput
import time

p2 = Picamera2()
video_config = p2.create_video_configuration()
p2.configure(video_config)

encoder = H264Encoder(repeat=True, iperiod=15)
out1 = FfmpegOutput("-f mpegts udp://<ip-address>:12345")
out2 = FileOutput()
encoder.output = [out1, out2]

p2.start_encoder(encoder)
p2.start()
time.sleep(5)

out2.fileoutput = "test.h264"
out2.start()
time.sleep(5)
out2.stop()

time.sleep(99999999)