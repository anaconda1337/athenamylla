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
    # Default resolutions of the frame are obtained.The default resolutions are system dependent.
    # We convert the resolutions from float to integer.
    frame_width = int(cam.get(3))
    frame_height = int(cam.get(4))
    # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
    out = cv2.VideoWriter('outpy.mp4',cv2.VideoWriter_fourcc(*'MP4V'), 20, (frame_width,frame_height))
    timeout = time.time() + (self.duration)
    while True:
      ret, frame = cam.read()
      if ret == True: 
        # Write the frame into the file 'output.avi'
        out.write(frame)
        # Display the resulting frame    
        cv2.imshow('frame',frame)
        if time.time() > timeout:
          break
      # Break the loop
      else:
        break 
    # When everything done, release the video capture and video write objects
    cam.release()
    out.release()
    # Closes all the frames
    cv2.destroyAllWindows()
    