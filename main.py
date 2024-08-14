import cv2
import torch
import time as t
# import csv
import os
from dotenv import load_dotenv
from datetime import *
import numpy as np
from scripts.getplate import *
from scripts.camera import Camera
from database.db import SaveDB
from LPR.hezar.models import Model
import random
import pytz
from scripts.filter import enhance_license_plate
import jdatetime
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath        


class PlateDetector:
    def __init__(self, camera_instance):
        self.camera_instance = camera_instance
        self.text_model = Model.load(hub_or_local_path=r'LPR', load_locally=True)
        self.model = torch.hub.load(r'yolov5', 'custom', path=r'models/myModel4.pt', source='local')
        self.width, self.height = 1280, 720
        self.capture_interval = 1
        self.model.max_det = 2
        # Calculate the coordinates for the two lines
        # self.line_y1, self.line_y2 = 30, 700
        self.line_y1, self.line_y2 = 0, 721
        # So that the model does not process if there is no license plate in the frame.
        self.not_plate = 0
        self.tehran_tz = pytz.timezone('Asia/Tehran')

    def detect_plates(self):
        start_time = t.time()
        capture_interval = 1  # seconds
        # video_capture = cv2.VideoCapture(self.camera_instance)
        
        while True:
            status = SaveDB().get_status()
            # ret, frame = video_capture.read()
            frame = self.camera_instance.get_frame()
            frame = cv2.resize(frame, (self.width, self.height))
            frame = frame[:, 250:1000]

            cv2.line(frame, (0, self.line_y1), (self.width, self.line_y1), (255, 0, 0), 2)
            cv2.line(frame, (0, self.line_y2), (self.width, self.line_y2), (255, 0, 0), 2)

            if status == 1:
                results = self.model(frame)
                predictions = results.pred[0]
                boxes = predictions[:, :4]
                
                car = f"dataset/captured_car_{random.randint(1, 9999)}.jpg"
                cv2.imwrite(car, frame)

                tehran_time = datetime.now(self.tehran_tz)
                shamsi_date = jdatetime.date.fromgregorian(date=tehran_time)
                date = shamsi_date.strftime('%Y/%m/%d')
                time = tehran_time.strftime('%H:%M:%S')
                CreateDateTime = f"{date}-{time}"
                
                plates_detected = 0
                yellow_plate = None

                for box in boxes:
                    x1, y1, x2, y2 = map(int, box)

                    if y1 > self.line_y1 and y2 < self.line_y2:
                        plates_detected += 1
                        plate_image = frame[y1:y2+9, x1:x2+9]
                        hsv_plate = cv2.cvtColor(plate_image, cv2.COLOR_BGR2HSV)
                        lower_yellow = np.array([20, 100, 100])
                        upper_yellow = np.array([30, 255, 255])
                        mask_yellow = cv2.inRange(hsv_plate, lower_yellow, upper_yellow)

                        if cv2.countNonZero(mask_yellow) > 0:
                            yellow_plate = (x1, y1, x2, y2, plate_image)

                print(f"{plates_detected} plates detected in the frame.")
                # So that the model does not process if there is no license plate in the frame.
                if plates_detected == 0:
                    self.not_plate += 1
                    if self.not_plate >= 5:
                        SaveDB().update_status(0)
                        self.not_plate = 0

                if plates_detected > 0:
                    if plates_detected > 1 and yellow_plate:
                        x1, y1, x2, y2, plate_image = yellow_plate
                    else:
                        x1, y1, x2, y2 = map(int, boxes[0])
                        plate_image = frame[y1:y2, x1:x2]

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                    plate_image = cv2.resize(plate_image, (300, 90))
                    current_time = t.time()

                    if current_time - start_time >= capture_interval:
                        try:
                            cv2.imwrite('MainPlate.jpg', enhance_license_plate(plate_image))
                            plate_text = self.text_model.predict(["MainPlate.jpg"])
                            plate = plate_text[0]['text']
                            plate = plate[::-1]
                            print(full_plate(plate))
                            # file = open('plates.csv', mode='r+', newline='', encoding='utf-8')
                            # reader = csv.reader(file)
                            try:
                                # rows = list(reader)
                                # if len(plate) > 7 and (len(rows) == 0 or plate != rows[-1][0]):
                                if len(plate) > 7:
                                    # file.seek(0, 2)
                                    # writer = csv.writer(file)
                                    # writer.writerow([plate, f'{date}-{time}'])
                                    image_name = f"view/plates/captured_plate_{random.randint(1, 9999)}.jpg"
                                    car = f"view/car/captured_car_{random.randint(1, 9999)}.jpg"
                                    cv2.imwrite(image_name, enhance_license_plate(plate_image))
                                    cv2.imwrite(car, frame)
                                    SaveDB().insert(Date=date, PlateFull=full_plate(plate), PlateNo=code_plate(plate), CreateDateTime=CreateDateTime)
                                    print(f"Image '{image_name}' captured.")
                                    SaveDB().update_status(0)
                            except Exception as e:
                                print(f"I can't recognize a license plate. Error: {e}")
                        except Exception as e:
                            print(f"Error capturing plate image: {e}")
                        # finally:
                        #     file.close()
                        start_time = current_time

            cv2.imshow('Leca Plate Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()
        SaveDB().update_status(0)

# PlateDetector(r'videos/bandicam 2024-07-09 10-55-01-429.mp4').detect_plates()
if __name__ == "__main__":
    load_dotenv() 
    camera = Camera(os.getenv('SOURCE'))
    PlateDetector(camera).detect_plates()
    camera.end()