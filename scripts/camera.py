import cv2
import multiprocessing as mp

class Camera():
    
    def __init__(self, rtsp_url):
        self.parent_conn, self.child_conn = mp.Pipe()
        self.p = mp.Process(target=self._update, args=(rtsp_url,))
        self.p.daemon = True
        self.p.start()

    def _update(self, rtsp_url):
        print("Cam Loading...")
        cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
        print("Cam Loaded...")
        run = True

        try:
            while run:
                cap.grab()
                rec_dat = self.child_conn.recv()
                if rec_dat == 1:
                    ret, frame = cap.read()
                    self.child_conn.send(frame)
                elif rec_dat == 2:
                    cap.release()
                    run = False

        except Exception as e:
            print(f"Error in camera process: {e}")
            
        finally:
            print("Camera Connection Closed")
            self.child_conn.close()

    def end(self):
        self.parent_conn.send(2)
        self.p.join()

    def get_frame(self, resize=None):
        self.parent_conn.send(1)
        frame = self.parent_conn.recv()
        self.parent_conn.send(0)

        if resize is not None:
            return self.rescale_frame(frame, resize)
        else:
            return frame

    def rescale_frame(self, frame, percent=5):
        return cv2.resize(frame, None, fx=percent, fy=percent)
