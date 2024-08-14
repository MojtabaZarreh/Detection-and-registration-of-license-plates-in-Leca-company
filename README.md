# License plate recognition on LECA company 🚚📹

This project is implemented in LECA company to register and identify car license plates on the weighing scale.


![msg24976722-26739](https://github.com/user-attachments/assets/bf9930f0-c34b-48b3-b29a-3d36fb4631f0)


I implemented this project at Leca Company using computer vision to enhance the speed of registering and processing the departure of loaded vehicles. After a click by the supervisors, the deep learning model is activated and begins processing and identifying the license plates. Once a plate is recognized in a frame, an image of the plate is captured and saved. Finally, the saved plate image is converted into text, extracting the plate numbers and characters, which are then stored in the company's database and displayed to the supervisors through the official company software.

I am also working on improving this system so that, with a single click, both the license plate and the vehicle's weight are simultaneously recorded in the company's software, eliminating the need for manual entry of the weight.



https://github.com/user-attachments/assets/956565f4-86a8-489e-ae2f-d5909ccdeaa6



https://github.com/user-attachments/assets/43cd0169-e813-422e-ab11-9bac87d1c022



# MODEL
YOLO version 5 is used to detect license plates in the images.

![YOLOv5_banner-1799x309](https://github.com/user-attachments/assets/d5e7c674-9c2e-4474-95d8-0cdb2b31c788)

And also, to convert the identified license plate images into text and extract numbers and letters from the image, the open text library named Hezar, whose model is C-RNN, has been used.

![hezar](https://github.com/user-attachments/assets/be91b3f4-21b8-4752-bf2a-0dd72843ece9)


# DATASET
The dataset used in this project is a collected dataset containing 2500 images of Iranian cars on the street and highways.
I do not have permission to publish this dataset.
(Special thanks to Ali Tavakalpour)

# RESOURCES

https://github.com/ultralytics/yolov5
https://pytorch.org/hub/ultralytics_yolov5/
https://huggingface.co/hezarai/crnn-fa-license-plate-recognition
https://github.com/hezarai/hezar
https://huggingface.co/keremberke/yolov5m-license-plate
https://huggingface.co/keremberke/yolov5s-license-plate
