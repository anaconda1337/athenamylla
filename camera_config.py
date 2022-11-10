import cv2
import time


class androidCamera(object):
  
  def __init__(self, duration):
    self.duration = duration
    pass
  
  def start_video(self):
    url = "https://IP-FROM-OPENCV-APPLICATION-ON-YOUR-PHONE/video"
    cam = cv2.VideoCapture(url)
    if (cam.isOpened() == False): 
      print("Unable to read camera feed")
    frame_width = int(cam.get(3))
    frame_height = int(cam.get(4))
    out = cv2.VideoWriter('outpy.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 20, (frame_width,frame_height))
    timeout = time.time() + (self.duration)
    while True:
      ret, frame = cam.read()
      if ret == True: 
        out.write(frame) 
        cv2.imshow('frame',frame)
        if time.time() > timeout:
          break
      else:
        break 
    cam.release()
    out.release()
    cv2.destroyAllWindows()
    
