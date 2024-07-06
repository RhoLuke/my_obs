import picamera2
import socket
import time
import os

video_file = "record.h264"

max_buffer_size = 1024*1024*1024

def start_stream():
    
    with picamera2.Picamera2() as camera:
        camera.resolution = (640,480)
        camera.framrate = 20
        
        server_socket = socket.socket()
        server_socket.bind(("0.0.0.0", 8000))
        server_socket.listen(0)
        
        connection = server_socket.accept()[0].makefile("wb")
        
        with open(video_file, "ab") as video_buffer:
            
            try:
                camera.start_recording(video_buffer, format="h264")
                buffer_size = video.buffer.tell()
                
                if buffer_size >= max_buffer_size:
                    video_buffer.seek(100*1024*1024)
                    remaining_data = video_buffer.read()
                    video_buffer.seek(0)
                    video_buffer.truncate()
                    video_buffer.write(reamining_data)
                time.sleep(1)
                
            finally:
                camera.stop_recording()
                connection.close()
                server_socket.close()

if __name__ == "__main__":
    start_stream()