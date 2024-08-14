import cv2
import torch
import time as t
import csv
from datetime import datetime
import numpy as np
from scripts.getplate import *
from scripts.camera import Camera
import threading
from database.db import SaveDB
import random
import pytz
from scripts.filter import enhance_license_plate
import jdatetime
from c_recognition.hezar.models import Model
from ultralytics import YOLO

def plate_detection(camera_instance):
    # video_capture = cv2.VideoCapture(camera_instance)
    text_model = Model.load(hub_or_local_path=r'c_recognition', load_locally=True)
    model = YOLO("bestV8.pt")
    model.max_det = 2 
    width, height = 1280, 720

    start_time = t.time()
    capture_interval = 1  # seconds
    line_y1 = 30
    line_y2 = 700
    not_plate = 0

    while True:
        status = SaveDB().get_status()
        # ret, frame = video_capture.read()
        frame = camera_instance.get_frame()
        frame = cv2.resize(frame, (width, height))
        frame = frame[:, 310:900]

        cv2.line(frame, (0, line_y1), (width, line_y1), (255, 0, 0), 2)
        cv2.line(frame, (0, line_y2), (width, line_y2), (255, 0, 0), 2)

        if status == 1:
            results = model(frame)

            tehran_tz = pytz.timezone('Asia/Tehran')
            tehran_time = datetime.now(tehran_tz)

            shamsi_date = jdatetime.date.fromgregorian(date=tehran_time)
            date = shamsi_date.strftime('%Y/%m/%d')
            time = tehran_time.strftime('%H:%M:%S')
            CreateDateTime = f"{date}-{time}"

            plates_detected = 0
            yellow_plate = None

            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    if y1 > line_y1 and y2 < line_y2:
                        plates_detected += 1

                        plate_image = frame[y1:y2, x1:x2]
                        hsv_plate = cv2.cvtColor(plate_image, cv2.COLOR_BGR2HSV)
                        lower_yellow = np.array([20, 100, 100])
                        upper_yellow = np.array([30, 255, 255])
                        mask_yellow = cv2.inRange(hsv_plate, lower_yellow, upper_yellow)

                        if cv2.countNonZero(mask_yellow) > 0:
                            yellow_plate = (x1, y1, x2, y2, plate_image)
                    
            print(f"{plates_detected} plates detected in the frame.")
            
            if plates_detected == 0:
                not_plate += 1
                if not_plate >= 5:
                    SaveDB().update_status(0)
                    not_plate = 0
                    
            if plates_detected > 0:
                if plates_detected > 1 and yellow_plate:
                    x1, y1, x2, y2, plate_image = yellow_plate
                else:
                    x1, y1, x2, y2 = map(int, result.boxes[0].xyxy[0])
                    plate_image = frame[y1:y2, x1:x2]

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                plate_image = cv2.resize(plate_image, (300, 90))
                current_time = t.time()
                if current_time - start_time >= capture_interval:
                    cv2.imwrite('MainPlate.jpg', enhance_license_plate(plate_image))
                    plate_text = text_model.predict(["MainPlate.jpg"])
                    plate = plate_text[0]['text']
                    plate = plate[::-1]
                    print(full_plate(plate))

                    with open('plates.csv', mode='r+', newline='', encoding='utf-8') as file:
                        reader = csv.reader(file)
                        rows = list(reader)
                        if len(plate) > 7 and (len(rows) == 0 or plate != rows[-1][0]):
                            writer = csv.writer(file)
                            writer.writerow([plate, f'{date}-{time}'])
                            image_name = f"view/plates/captured_plate_{random.randint(1, 9999)}.jpg"
                            car = f"view/car/captured_car_{random.randint(1, 9999)}.jpg"
                            cv2.imwrite(image_name, enhance_license_plate(plate_image))
                            cv2.imwrite(car, frame)
                            SaveDB().insert(Date=date, PlateFull=full_plate(plate), PlateNo=code_plate(plate), CreateDateTime=CreateDateTime)
                            print(f"Image '{image_name}' captured.")
                            SaveDB().update_status(0)
                    start_time = current_time

        cv2.imshow('Leca Plate Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    SaveDB().update_status(0)

# plate_detection(r'videos/test6.mp4')
if __name__ == "__main__":
    rtsp_url = 'rtsp://admin:leca@1403@192.168.61.43/'
    camera = Camera(rtsp_url)
    plate_detection(camera)
