from __future__ import print_function
import os
import io
import tensorflow as tf
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
import cv2
from google.cloud import vision
import numpy as np
import requests
import uuid
import time
from tkinter import *
from PIL import Image, ImageTk

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'TFOD/credentials.json'                          #Set credentials for Google Vision API
MODEL_NAME = 'mymobnetssd'                                                                       #Define TensorFlow model name                                                             

paths = {
    'ANNOTATION_PATH': os.path.join('TFOD','Tensorflow', 'workspace','annotations'),             #Define path to Annotation credentials - [labelmap and TensorFlow record files]
    'CHECKPOINT_PATH': os.path.join('TFOD','Tensorflow', 'workspace','models',MODEL_NAME)        #Define path to get checkpoint file obtained after training.
 }

files = {
    'PIPELINE_CONFIG':os.path.join('TFOD','Tensorflow', 'workspace','models', MODEL_NAME, 'pipeline.config'),
    'LABELMAP': os.path.join(paths['ANNOTATION_PATH'], 'label_map.pbtxt')
}
                                                                                                 #Load pipeline config and build a detection model
configs = config_util.get_configs_from_pipeline_file(files['PIPELINE_CONFIG'])
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

###################### EXISTING CODE USED FROM EXTERNAL SOURCE############################                                                                                                #Restore checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(paths['CHECKPOINT_PATH'], 'ckpt-16')).expect_partial()
                                                                                            #Raw Detections
#@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections
category_index = label_map_util.create_category_index_from_labelmap(files['LABELMAP'])           #This line gives index for back and front regPlate.
                                                                                                 #Easy OCR Function
def detect_text(image, detections):
    detection_threshold = 0.7                                                                    #Only OCR detections above this threshold will be outputted
    scores = list(filter(lambda x: x> detection_threshold, detections['detection_scores']))      #Filters through the detections array for values that are only above threshold
    boxes = detections['detection_boxes'][:len(scores)]                                          #Filter through the amount of detected boxes by the amount of scores that have passed the threshold
                                                                                                 #Note : The variable image is the WHOLE frame NOT the Region of Interest- NumPlate
    height = image.shape[0]                                                                      #Get height of whole image
    width = image.shape[1]                                                                       #Get width of whole image
                                                                                                 #Apply Region of Interest filtering - Crop the image into the Number Plate section
    for index, box in enumerate(boxes):                                                          #Loop through every box
        roi = box * [height, width, height, width]                                               #Box coordinates are not with respect to actual size of image so multipy to get actual coords - they are repect to a 1 x 1 box
        try:
            region = image[int(roi[0]):int(roi[2]),int(roi[1]):int(roi[3])]                      #Plot ROI Coords onto whole image - Crop
        except:
            pass
                                                                                                 #Save Image to directory
        img_name = '{}.jpg'.format(uuid.uuid1())                                                 #Assign random name to the ROI
        folder_path = 'TFOD/OutputImages'                                                        #Define folder path for location to store images
        cv2.imwrite(os.path.join(folder_path, img_name), region)                                 #Store image

###################### EXTERNAL CODE ENDS HERE############################
                                                                                                 #GOOGLE VISION API
        client = vision.ImageAnnotatorClient()                                                   #Define client      
        filepath = os.path.join(folder_path, img_name)                                           #Use image stored and text detect from that image
        with io.open(filepath, 'rb') as image_file:                                              #Open image and read
            content = image_file.read()

        image = vision.Image(content=content)              

        response = client.text_detection(image=image)                                            #Get response
        texts = response.text_annotations       
        detected_registration_plate = texts[0].description                                       #Print reponse
        #print('\n"{}"'.format(texts[0].description))

        if response.error.message:                                                               #If error return exception
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

        #plt.imshow(cv2.cvtColor(region, cv2.COLOR_BGR2RGB))
        #matplotlib.use('TkAgg')
        #plt.show()

        if(detected_registration_plate[2] == "I"):
            detected_registration_plate = detected_registration_plate[0:2] + "1" + detected_registration_plate[3:8]

        if(detected_registration_plate[3] == "I"):
            detected_registration_plate = detected_registration_plate[0:3] + "1" + detected_registration_plate[4:8]

        if(detected_registration_plate[2] == "O"):
            detected_registration_plate = detected_registration_plate[0:2] + "0" + detected_registration_plate[3:8]
        
        if(detected_registration_plate[3] == "O"):
            detected_registration_plate = detected_registration_plate[0:3] + "0" + detected_registration_plate[4:8]


        validation = validatePlate(detected_registration_plate)

        if( validation == True):
            return detected_registration_plate
        else:
            return None

def validatePlate(plate):                                                                        #Function to validate whether a text extracttion has detected a valid plate
    plateValid = True
    #Length of string                                                                            #The plate should be a length of 8 characters
    if(len(plate) != 8):
        plateValid == False
        #print("1")

    #First 2 letters                                                                             #The first 2 characters of the plate should be uppercase alphabet characters 
    first2Chars = str(plate[0:2])
    for x in first2Chars:
        if(ord(str(x)) not in range(64,91)):                                                     #CHecks whether the ASCII value is in the correct range
            plateValid = False
            #print("2")

    #Third and Fourth numbers                                                                    #The 3rd and 4th chracters should be numerical values
    numbers = str(plate[2:4])
    for y in numbers:
        if(ord(str(y)) not in range(47,58)):
            plateValid = False
            #print("3")
    
    #Space                                                                                       #There should be a space in the 5th character
    if (plate[4].isspace() == False):
        plateValid = False
        #print("4")

    #Last 3 Chars                                                                                #The final 3 characters should be alphabetical values
    threeChars = str(plate[5:8])
    for z in threeChars:
        if(ord(str(z)) not in range(64,91)):
            plateValid = False
            #print("5")

    if plateValid == True:
        return True
    else:
        return False

def vehicleLookup(numberPlate):
    url = 'https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles'
    head = {'x-api-key':'U8eDaSElCE5V5doIvCQmP95TVOzNEXiM1pZ5jh47', 'Content-Type':'application/json'}
    body = {'registrationNumber': numberPlate}
    try:
        x = requests.post(url, json = body, headers=head)
        parsed = x.text.split(',')
        for parameter in parsed:
            print(parameter)
    except:
        return None

videoPath = os.path.join('TFOD','TestVideos', 'test7.mp4')
cap = cv2.VideoCapture(0)                                                                        #Define video input - [enter 0 for camera else put file path of video file]
plateDetected = False
root = Tk()
root.title("Video")
label = Label(root)
label.grid(row=0, column=0)


#while cap.isOpened():  
#while plateDetected == False: 
def detect():                                                                   #While the video source is open do this
    ret, frame = cap.read()
    image_np = np.array(frame)
    image_np_expanded = np.expand_dims(frame, axis=0)

    input_tensor = tf.convert_to_tensor(image_np_expanded, dtype=tf.float32)
    detections = detect_fn(input_tensor)

    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                for key, value in detections.items()}
    detections['num_detections'] = num_detections

    # detection_classes should be ints.
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    label_id_offset = 1
    image_np_with_detections = image_np.copy()  
    viz_utils.visualize_boxes_and_labels_on_image_array(                                         #Call tensorflow viz.utils function - this visualises and draws the bozes on detections in real time
        image_np_with_detections,
        detections['detection_boxes'],
        detections['detection_classes'] + label_id_offset,
        detections['detection_scores'],
        category_index,
        use_normalized_coordinates=True,
        max_boxes_to_draw=1,
        min_score_thresh=.25,                                                                    #Set minimum threshold for a detection to be valid
        agnostic_mode=False)
    numberPlate = detect_text(image_np_with_detections, detections)

    if numberPlate != None:
        print(numberPlate)
        plateDetected = True        
                                                                                                #Call text detection function with ROI 

    cv2image= cv2.cvtColor(image_np_with_detections,cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(img)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    root.after(25, detect)

detect()
root.mainloop()

#print("The detected number plate is {}".format(numberPlate))
#print("---------------------------------------------------------------Looking Up DVLA------------------------------------------------------------------------")
#vehicleLookup(numberPlate)
#print("------------------------------------------------------------------------------------------------------------------------------------------------------")


