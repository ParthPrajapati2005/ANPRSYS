import tkinter as tk
from tkinter import *
from tkinter import font as tkFont
from tkinter import filedialog
import customtkinter
import numpy as np
import mysql.connector
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder
from object_detection.utils import config_util
from urllib.request import Request, urlopen
import tensorflow as tf
import os
import cv2
import io
import time
import json
import requests
from PIL import Image, ImageTk
from google.cloud import vision
import uuid

class detectPage(tk.Canvas):
    prevmast = ()
    workspace = ()
    carImage = ()
    logoImage = ()
    currentWorkspace = ""
    finalPlate = ""
    plateImage = ""
    roi = ()
    plateDetected = False
    videoModeVar = False
    cap = cv2.VideoCapture(0)                                                                 #Define video input - [enter 0 for camera else put file path of video file]

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'TFOD/credentials.json'                          #Set credentials for Google Vision API
    #MODEL_NAME = 'mymobnetssd'  
    MODEL_NAME = 'my_centernet' 
    paths = {
                'ANNOTATION_PATH': os.path.join('TFOD','Tensorflow', 'workspace','annotations'),             #Define path to Annotation credentials - [labelmap and TensorFlow record files]
                'CHECKPOINT_PATH': os.path.join('TFOD','Tensorflow', 'workspace','models',MODEL_NAME)        #Define path to get checkpoint file obtained after training.
            }

    files = {
                'PIPELINE_CONFIG':os.path.join('TFOD','Tensorflow', 'workspace','models', MODEL_NAME, 'pipeline.config'),
                'LABELMAP': os.path.join(paths['ANNOTATION_PATH'], 'label_map.pbtxt')
            }

    configs = config_util.get_configs_from_pipeline_file(files['PIPELINE_CONFIG'])
    detection_model = model_builder.build(model_config=configs['model'], is_training=False)

    ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)                                      #Restore checkpoint
    ckpt.restore(os.path.join(paths['CHECKPOINT_PATH'], 'ckpt-51')).expect_partial()
    category_index = label_map_util.create_category_index_from_labelmap(files['LABELMAP'])           #This line gives index for back and front regPlate.                                                                                             #Raw Detections
    @tf.function
    def detect_fn(self,image):
        image, shapes = self.detection_model.preprocess(image)
        prediction_dict = self.detection_model.predict(image, shapes)
        detections = self.detection_model.postprocess(prediction_dict, shapes)
        return detections
                                                                                                     
    def detect_text(self, image, detections):
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
            img_name = '{}.jpg'.format(uuid.uuid1())    
            self.plateImage = img_name                                                               #Assign random name to the ROI
            folder_path = 'TFOD/OutputImages'                                                        #Define folder path for location to store images
            cv2.imwrite(os.path.join(folder_path, img_name), region)                                 #Store image
                                                                                                     #GOOGLE VISION API
            client = vision.ImageAnnotatorClient()                                                   #Define client      
            filepath = os.path.join(folder_path, img_name)                                           #Use image stored and text detect from that image
            with io.open(filepath, 'rb') as image_file:                                              #Open image and read
                content = image_file.read()

            image = vision.Image(content=content)              

            try:
                response = client.text_detection(image=image)                                            #Get response
                texts = response.text_annotations       
                detected_registration_plate = texts[0].description                                       #Print reponse
            except:
                detected_registration_plate = "Invalid"

            if response.error.message:                                                               #If error return exception
                raise Exception(
                    '{}\nFor more info on error messages, check: '
                    'https://cloud.google.com/apis/design/errors'.format(
                        response.error.message))


            if(detected_registration_plate[2] == "I"):
                detected_registration_plate = detected_registration_plate[0:2] + "1" + detected_registration_plate[3:8] #If 3rd character is I then change to 1

            if(detected_registration_plate[3] == "I"):
                detected_registration_plate = detected_registration_plate[0:3] + "1" + detected_registration_plate[4:8] #If 4rd character is I then change to 1

            if(detected_registration_plate[2] == "O"):
                detected_registration_plate = detected_registration_plate[0:2] + "0" + detected_registration_plate[3:8] #If 3rd character is O then change to 0
            
            if(detected_registration_plate[3] == "O"):
                detected_registration_plate = detected_registration_plate[0:3] + "0" + detected_registration_plate[4:8] #If 4rd character is O then change to 0

            try:
                validation = self.validatePlate(detected_registration_plate)    #Call the validation function
            except:
                pass

            if( validation == True):                    #If validation checks pass then return detected plate
                return detected_registration_plate
            else:
                return None

    def validatePlate(self, plate):               #Function to validate whether a text extracttion has detected a valid plate
        plateValid = True
        #Length of string                      #The plate should be a length of 8 characters
        if(len(plate) != 8):
            plateValid == False
            #print("1")

        #First 2 letters                           #The first 2 characters of the plate should be uppercase alphabet characters 
        first2Chars = str(plate[0:2])
        for x in first2Chars:
            if(ord(str(x)) not in range(64,91)):   #Checks whether the ASCII value is in the correct range
                plateValid = False
                #print("2")

        #Third and Fourth numbers                  #The 3rd and 4th chracters should be numerical values
        numbers = str(plate[2:4])
        for y in numbers:
            if(ord(str(y)) not in range(47,58)):
                plateValid = False
                #print("3")
        
        #Space                                    #There should be a space in the 5th character
        if (plate[4].isspace() == False):
            plateValid = False
            #print("4")

        #Last 3 Chars                             #The final 3 characters should be alphabetical values
        threeChars = str(plate[5:8])
        for z in threeChars:
            if(ord(str(z)) not in range(64,91)):
                plateValid = False
                #print("5")

        if plateValid == True:
            return True
        else:
            return False

    def vehicleLookup(self):
        body = {"registrationPlate" : str(self.finalPlate)}         #Prepare the pauload for the POST request
        status = 0
        req1 = requests.post('https://vehicle-api-parth13075.vercel.app/getImages', json=body)  #Send request to both Image API's to try and get vehicle Images
        req1a = requests.post('https://vehicle-api-parth13075.vercel.app/getImages2', json=body)

        if req1.status_code == 200:                         #If successful, then store URL in variable
            vehicleImages = json.loads(req1.text)
        else:
            vehicleImages = json.loads(req1a.text)          #Else, use url from second link
            
        vehicleImageURL = vehicleImages["carImageURL"]      #Extract both vehicle and logo image urls from response
        vehicleLogoURL = vehicleImages["logoImageURL"]

        req2 = requests.post('https://vehicle-api-parth13075.vercel.app/depthCheckAPI', json=body)      #Send request to get vehicle details 
        req2a = requests.post('https://vehicle-api-parth13075.vercel.app/depthCheckAPI2', json=body)

        if req2.status_code == 200:                     #If successful store response
            vehicleDetails = json.loads(req2.text)
            status = 1
        else:
            vehicleDetails = json.loads(req2a.text)    #Else use data from secind link
            status = 2

        req3 = requests.post('https://vehicle-api-parth13075.vercel.app/getMileageHistory', json=body)
        vehicleMileages = json.loads(req3.text)

        return vehicleImageURL, vehicleLogoURL, vehicleDetails, vehicleMileages, status

    def displayDetails(self):

        def reset():
            self.prevmast.switchFrame("detectPage")
            
        def createDatabaseRecord():
            user_email = self.prevmast.detectionUser            #Get username and password from global variables
            user_password = self.prevmast.detectionPassword

            mydb = mysql.connector.connect(                     #Connect to database as user
            host="132.145.65.198",
            user=user_email,
            password=user_password,
            auth_plugin='mysql_native_password',
            database= "anprDATABASE"
            )

            mycursor = mydb.cursor()                            #DB Object  
            mycursor.execute("SHOW TABLES;")
            table = (mycursor.fetchone()[0]).decode("utf-8")

            gmt = time.gmtime(time.time())                              #Get current date and time
            if len(str(gmt[1])) == 1:
                currentDate = "0"+str(gmt[1])+"-"+str(gmt[2])+"-"+str(gmt[0])
            else:
                currentDate = str(gmt[1])+"-"+str(gmt[2])+"-"+str(gmt[0])
            currentTime = str(gmt[3])+":"+str(gmt[4])
            #date and time format
            #'13:30', '1-28-2018'

            if status == 1:                                        #Construct SQL query
                command = """INSERT INTO """+table+""" (
                    registrationPlate,
                    dateOfDetection,
                    timeOfDetection,
                    vehicleMake,
                    vehicleModel,
                    vehicleColour,
                    vehicleFuelType,
                    vehicleType,
                    vehicleBodyType,
                    vehicleExported,
                    vehicleTopSpeed,
                    vehicle60Time,
                    vehicleEngineCapacity,
                    vehicleHorsepower,
                    vehicleEstimatedMileage,
                    vehicleInsuranceGroup,
                    vehicleAge,
                    vehicleYOM,
                    vehicleSalvage,
                    vehicleMOTDue,
                    vehicleTAXDue,
                    vehicleCarbonEmissions,
                    vehicleFuelEconomy,
                    vehicleTaxCost) VALUES (%s,STR_TO_DATE(%s,'%m-%d-%Y'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

                values = (vehicleDetails["Registration Plate"],         #Insert all values into SQL query
                          currentDate,
                          currentTime,
                          vehicleDetails["Make"],
                          vehicleDetails["Model"],
                          vehicleDetails["Colour"],
                          vehicleDetails["Fuel"],
                          vehicleDetails["Vehicle Type"],
                          vehicleDetails["Body Type"],
                          vehicleDetails["Exported Vehicle"],
                          vehicleDetails["Top Speed"],
                          vehicleDetails["0-60mph Time"],
                          vehicleDetails["Engine Capacity"],
                          vehicleDetails["Horsepower"],
                          vehicleDetails["Estimated Current Mileage"],
                          vehicleDetails["Insurance Group"],
                          (vehicleDetails["Vehicle Age"])[1:],
                          vehicleDetails["Year of Manufacture"],
                          vehicleDetails["Salvage History"],
                          vehicleDetails["MOT Due"],
                          vehicleDetails["TAX Due"],
                          vehicleDetails["Carbon Emissions"],
                          vehicleDetails["Combined Fuel Economy"],
                          vehicleDetails["Average Tax Cost (12 Months)"])

                if self.recordCreated == False:
                    mycursor.execute(command, values)
                    mydb.commit()
                    self.recordCreated = True
                

            elif status == 2:
                command = """INSERT INTO """+table+""" (
                    registrationPlate,
                    dateOfDetection,
                    timeOfDetection,
                    vehicleMake,
                    vehicleModel,
                    vehicleColour,
                    vehicleFuelType,
                    vehicleType,
                    vehicleBodyType,
                    vehicleExported,
                    vehicleTopSpeed,
                    vehicle60Time,
                    vehicleEngineCapacity,
                    vehicleHorsepower,
                    vehicleInsuranceGroup,
                    vehicleYOM,
                    vehicleMOTDue,
                    vehicleTAXDue,
                    vehicleTaxCost) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            
                values = (vehicleDetails["Registration Plate"],
                          currentDate,
                          currentTime,
                          vehicleDetails["make"],
                          vehicleDetails["model"],
                          vehicleDetails["colour"],
                          vehicleDetails["fuelType"],
                          vehicleDetails["vehicleType"],
                          vehicleDetails["bodyType"],
                          vehicleDetails["Exported"],
                          vehicleDetails["topSpeed"],
                          vehicleDetails["0-60mph"],
                          vehicleDetails["engineCapacity"],
                          vehicleDetails["horsepower"],
                          vehicleDetails["insuranceGroup"],
                          vehicleDetails["yearOfManufacture"],
                          vehicleDetails["motExpiry"],
                          vehicleDetails["taxExpiry"],
                          vehicleDetails["taxCost12Months"])

                if self.recordCreated == False:
                    mycursor.execute(command, values)
                    mydb.commit()
                    self.recordCreated = True

        vehicleImageURL, vehicleLogoURL, vehicleDetails, vehicleMileages, status = self.vehicleLookup()

        displayWorkspace = ()
        
        if self.currentWorkspace == "live":
            com = Label(self.liveWorkspace, text="DETECTION COMPLETE!", fg="lime", bg="#141B2D", font=("Azonix", 40), anchor="center")
            com.pack()
            displayWorkspace = Canvas(self.liveWorkspace, height=self.winfo_screenheight()-50, width=self.winfo_screenwidth()-100, bg="#141B2D", highlightthickness=False)
            displayWorkspace.pack(side="left")

        if self.currentWorkspace == "video":
            com = Label(self.videoWorkspace, text="DETECTION COMPLETE!", fg="lime", bg="#141B2D", font=("Azonix", 40), anchor="center")
            com.pack()
            displayWorkspace = Canvas(self.videoWorkspace, height=self.winfo_screenheight()-50, width=self.winfo_screenwidth()-100, bg="#141B2D", highlightthickness=False)
            displayWorkspace.pack(side="left")

        #Display details from first link
        if status == 1:
            displayWorkspace.create_text(100,50,text=("REGISTRATION PLATE : "+vehicleDetails["Registration Plate"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,80,text=("MAKE : "+vehicleDetails["Make"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,110,text=("MODEL : "+vehicleDetails["Model"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,140,text=("COLOUR : "+vehicleDetails["Colour"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,170,text=("FUEL : "+vehicleDetails["Fuel"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,200,text=("VEHICLE TYPE : "+vehicleDetails["Vehicle Type"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,230,text=("BODY TYPE : "+vehicleDetails["Body Type"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,260,text=("EXPORTED VEHICLE : "+vehicleDetails["Exported Vehicle"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,290,text=("TOP SPEED : "+vehicleDetails["Top Speed"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,320,text=("0 - 60MPH TIME : "+vehicleDetails["0-60mph Time"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,350,text=("ENGINE CAPACITY : "+vehicleDetails["Engine Capacity"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,380,text=("HORSEPOWER : "+vehicleDetails["Horsepower"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,410,text=("ESTIMATED CURRENT MILEAGE : "+vehicleDetails["Estimated Current Mileage"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,440,text=("INSURANCE GROUP : "+vehicleDetails["Insurance Group"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,470,text=("VEHICLE AGE : "+(vehicleDetails["Vehicle Age"])[1:]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,500,text=("YEAR OF MANUFACTURE : "+vehicleDetails["Year of Manufacture"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,530,text=("SALVAGE HISTORY : "+vehicleDetails["Salvage History"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,560,text=("MOT DUE ON : "+vehicleDetails["MOT Due"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,590,text=("TAX DUE ON : "+vehicleDetails["TAX Due"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,620,text=("CARBON EMMISIONS : "+vehicleDetails["Carbon Emissions"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,650,text=("FUEL ECONOMY : "+vehicleDetails["Combined Fuel Economy"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,680,text=("AVERAGE TAX COST (12 MONTHS) : "+vehicleDetails["Average Tax Cost (12 Months)"]), font=("Modern_Mono",20), fill="white", anchor="nw")

        #Display details from second link
        elif status == 2:
            displayWorkspace.create_text(100,50,text=("REGISTRATION PLATE : "+vehicleDetails["Registration Plate"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,80,text=("MAKE : "+vehicleDetails["make"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,110,text=("MODEL : "+vehicleDetails["model"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,140,text=("COLOUR : "+vehicleDetails["colour"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,170,text=("FUEL : "+vehicleDetails["fuelType"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,200,text=("VEHICLE TYPE : "+vehicleDetails["vehicleType"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,230,text=("BODY TYPE : "+vehicleDetails["bodyType"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,260,text=("EXPORTED VEHICLE : "+vehicleDetails["Exported"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,290,text=("TOP SPEED : "+vehicleDetails["topSpeed"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,320,text=("0 - 60MPH TIME : "+vehicleDetails["0-60mph"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,350,text=("ENGINE CAPACITY : "+str(vehicleDetails["engineCapacity"])), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,380,text=("HORSEPOWER : "+vehicleDetails["horsepower"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,410,text=("INSURANCE GROUP : "+vehicleDetails["insuranceGroup"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,440,text=("YEAR OF MANUFACTURE : "+str(vehicleDetails["yearOfManufacture"])), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,500,text=("MOT : "+vehicleDetails["motExpiry"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,530,text=("TAX : "+vehicleDetails["taxExpiry"]), font=("Modern_Mono",20), fill="white", anchor="nw")
            displayWorkspace.create_text(100,560,text=("AVERAGE TAX COST (12 MONTHS) : "+vehicleDetails["taxCost12Months"]), font=("Modern_Mono",20), fill="white", anchor="nw")

        self.recordCreated = False
        carImage = Image.open(requests.get(vehicleImageURL, stream = True).raw) #Load and display car images from url
        resizedCarImage = carImage.resize((600,400),Image.ANTIALIAS)
        self.carImage = ImageTk.PhotoImage(resizedCarImage)

        logoImage = Image.open(requests.get(vehicleLogoURL, stream=True).raw)   #Load and display logo image from url
        resizedLogoImage = logoImage.resize((300, 200), Image.ANTIALIAS)
        self.logoImage = ImageTk.PhotoImage(resizedLogoImage)

        roiPath = os.path.join("TFOD", "OutputImages", self.plateImage)  #Store the cropper roi image to directory
        roiImage = Image.open(roiPath)
        resizedROI = roiImage.resize((200, 100), Image.ANTIALIAS)        #Resize it for the GUI
        self.roi = ImageTk.PhotoImage(resizedROI)

        displayWorkspace.create_image(1000, 250, image=self.carImage)   #Display and position all 3 images
        displayWorkspace.create_image(1600, 250, image=self.logoImage)
        displayWorkspace.create_image(1000, 600, image=self.roi)

        buttonWorkspace = Frame(displayWorkspace, height=300, width=550, highlightthickness=False, bg="#141B2D") #Create workspace for button
        buttonWorkspace.pack()
        displayWorkspace.create_window(1500,550, window=buttonWorkspace)

        resetButton = customtkinter.CTkButton(buttonWorkspace, text="DETECT AGAIN", height=80, width=200, bg="#141B2D", command=reset) #Button to do another detection
        resetButton.pack()  

        databaseButton = customtkinter.CTkButton(buttonWorkspace, text="CREATE DATABASE RECORD", height=80, width=200, bg="#141B2D", command=createDatabaseRecord)
        databaseButton.pack(pady=30)

    def loadingFrame(self, status):
        if status == True:              #If function is called with status var = True then show loading screen
            self.loaded = False         #Boolean variable set as false as it has not loaded
            load = Label(self.liveFeed, text="Interface Loading.....", font=("Azonix", 40), bg="#141B2D", fg="white")   #Display message
            load.pack(padx=190, pady=300)   #Pack the message
            self.liveFeed.pack(padx=380)    #Load the camera feed onto the workspace

        if status == False and self.loaded == False:    #If function is called with status = True
            self.loaded = True
            for widgets in self.liveFeed.winfo_children():  #Destroy everything in livefeed
                widgets.destroy()
            
            detectionsLabel = Label(self.liveWorkspace, text="LIVE DETECTIONS ON", fg="lime", font=("Modern_Mono",25), bg="#141B2D") #Info message
            detectionsLabel.pack(padx=10)   #Pack the message
            
    def detect(self):
        if self.finalPlate != "" and self.plateDetected == True:        #If the plate has been detected, destroy the video feed
            self.liveFeed.destroy()
            for widgets in self.liveWorkspace.winfo_children():         #Destroy everything in the workspace
                widgets.destroy()
            self.displayDetails()                                       #Call function to display the vehicle details

        if self.plateDetected == False:             #If plate has not been detected
            ret, frame = self.cap.read()
            image_np = np.array(frame)
            image_np_expanded = np.expand_dims(frame, axis=0)

            input_tensor = tf.convert_to_tensor(image_np_expanded, dtype=tf.float32)
            detections = self.detect_fn(input_tensor)

            num_detections = int(detections.pop('num_detections'))
            detections = {key: value[0, :num_detections].numpy()
                        for key, value in detections.items()}
            detections['num_detections'] = num_detections

            # detection_classes should be ints.
            detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
            category_index = label_map_util.create_category_index_from_labelmap(self.files['LABELMAP'])
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
            numberPlate = self.detect_text(image_np_with_detections, detections)                        #Call function for text extraction 

            if numberPlate != None:                 #If a number plate is returned from text extraction then print it
                print(numberPlate)
                self.finalPlate = numberPlate       #store number plate in variable
                self.plateDetected = True           #set plate found = true

            self.loadingFrame(status=False)                        #Call loading page function with status = False to show that the detection funtion has loaded
            resized = cv2.resize(image_np_with_detections,(1000, 700))  #Resize the image to the liveFeed dimenstions
            cv2image= cv2.cvtColor(resized,cv2.COLOR_BGR2RGB)           #Convert the image to colour
            img = Image.fromarray(cv2image)                             #Turn array into image
            imgtk = ImageTk.PhotoImage(img)                             #Turn image into tkinter image object
            self.liveFeed.imgtk = imgtk                                 #Configure the livefeed workspace to show image frame on GUI
            self.liveFeed.configure(image=imgtk)
            self.after(15, self.detect)                                 #Call detection function all again with next frame

    def __init__(self, master):
        tk.Canvas.__init__(self, master)
        self.prevmast = master
        screenwidth = master.winfo_screenwidth()
        screenheight = master.winfo_screenheight()
        master.geometry("{}x{}+{}+{}".format(screenwidth, screenheight,-1,1))
        self.prevmast.title("ANPR - Automatic Number Plate Recognition System") 

        screen = Canvas(self, highlightthickness=False, width=screenwidth, height=screenheight, bg="#141B2D") ##141B2D
        
        screen.icon_filePaths = {'dashboard-icon':os.path.join('GUI','Icons', 'dashboard-icon-48.png'),
                          'detect-icon':os.path.join('GUI','Icons', 'detect-icon-48.png'),
                          'detect-icon-blue':os.path.join('GUI','Icons', 'detect-icon-blue-48.png'),
                          'database-icon':os.path.join('GUI','Icons', 'database-icon-48.png'),
                          'search-icon':os.path.join('GUI','Icons', 'search-icon-48.png'),
                          'mot-icon':os.path.join('GUI','Icons', 'mot-icon-48.png'),
                          'settings-icon':os.path.join('GUI','Icons', 'settings-icon-48.png'),
                          'logoff-icon':os.path.join('GUI','Icons', 'logoff-icon-48.png'),
                          'empty-icon':os.path.join('GUI','Icons', 'empty-icon-48.png')}
        
        screen.icon_renders = {'dashboard-icon':ImageTk.PhotoImage(image=Image.open(screen.icon_filePaths['dashboard-icon'])),
                        'detect-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['detect-icon-blue'])),
                        'database-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['database-icon'])),
                        'search-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['search-icon'])),
                        'mot-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['mot-icon'])),
                        'settings-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['settings-icon'])),
                        'logoff-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['logoff-icon'])),
                        'empty-icon':ImageTk.PhotoImage(master=screen, image=Image.open(screen.icon_filePaths['empty-icon']))}

        screen.create_rectangle(0,0,100,screenheight, fill="#1F2940", outline="")   #212325

        dashboardButton = screen.create_image(50,50,image=screen.icon_renders['dashboard-icon'])
        screen.tag_bind(dashboardButton, "<Button-1>", self.switchDashboard)
        screen.create_text(50, 100, text="Dashboard", font=("Modern_Mono",15), fill='white')
        
        detectButton = screen.create_image(50, 200, image=screen.icon_renders['detect-icon'])
        screen.tag_bind(detectButton, "<Button-1>", self.switchDetect)
        screen.create_text(50, 250, text="Detect", font=("Modern_Mono",15), fill='white')

        databaseButton = screen.create_image(50,350, image=screen.icon_renders['database-icon'])
        screen.tag_bind(databaseButton, "<Button-1>", self.switchDatabase)
        screen.create_text(50, 400, text="Database", font=("Modern_Mono",15), fill='white')

        searchButton = screen.create_image(50,500, image=screen.icon_renders['search-icon'])
        screen.tag_bind(searchButton, "<Button-1>", self.switchSearch)
        screen.create_text(50, 550, text="Search", font=("Modern_Mono",15), fill='white')

        motButton = screen.create_image(50,650, image=screen.icon_renders['mot-icon'])
        screen.tag_bind(motButton, "<Button-1>", self.switchMOT)
        screen.create_text(50, 700, text="MOT", font=("Modern_Mono",15), fill='white')

        settingsButton = screen.create_image(50,800, image=screen.icon_renders['settings-icon'])
        screen.tag_bind(settingsButton, "<Button-1>", self.switchSettings)
        screen.create_text(50, 850, text="Settings", font=("Modern_Mono",15), fill='white')

        logoffButton = screen.create_image(50,950, image=screen.icon_renders['logoff-icon'])
        screen.tag_bind(logoffButton, "<Button-1>", self.switchLogoff)
        screen.create_text(50, 1000, text="Log Off", font=("Modern_Mono",15), fill='white')

        screen.pack(side=LEFT)

        self.workspace = Canvas(screen, height=self.winfo_screenheight(), width=self.winfo_screenwidth()-100, highlightthickness=False, bg="#141B2D")
        self.workspace.pack()

        self.workspace.place(x=100, y=0)

        self.build()
    
    def build(self): # Function to create radiobuttons for modes.
        self.workspace.create_text(50, 60, fill="white", text="DETECT", font=("Azonix", 40), anchor='w')    #Page title
        #Create a separatecanvas workpace only for the radio buttons
        radioButton_workspace = customtkinter.CTkCanvas(self.workspace, height=self.winfo_screenheight()-200, width=self.winfo_screenwidth()-100) 
        radioButton_workspace.configure(bg="#141B2D", highlightthickness=False)     #Set background color and disable borders
        radioButton_workspace.place(x=50,y=120) #Position the workspace.
        radioVar = tk.IntVar(value=0)   #Create a variable which contains the current selected radio button

        #Create a separate workspace which will contain the detection space and make it global
        self.mainWorkspace = customtkinter.CTkCanvas(self.workspace, width=self.winfo_screenwidth(), height = self.winfo_screenheight()-200)
        self.mainWorkspace.config(bg="#141B2D", highlightthickness=False)
        self.mainWorkspace.place(x=0, y=200)
        self.mainWorkspace.create_text(350, 350, fill="white", text="SELECT ONE OF THE MODES ABOVE", font=("Azonix", 40), anchor='w') #Info message

        #Create 2 frames for the 2 different modes and contain them in the mainWorkspace - global
        self.liveWorkspace = Frame(self.mainWorkspace, width=self.winfo_screenwidth(), height = self.winfo_screenheight()-200, bg="#141B2D") 
        self.videoWorkspace = Frame(self.mainWorkspace, width=self.winfo_screenwidth(), height = self.winfo_screenheight()-200, bg="#141B2D")
        
        liveRadButton = customtkinter.CTkRadioButton(master=radioButton_workspace,      #Create Radio button for live mode
                                                     variable=radioVar,                 #Fefine variable
                                                     value=0, 
                                                     text="Live Mode",                  #Caption
                                                     text_font="Modern_Mono",           #Font
                                                     command=self.liveMode)             #Call self.liveMode funtion when pressed

        liveRadButton.grid(row=1, column=2, pady=10, padx=20, sticky="n")               #Pack the radio button onto the page.

        videoRadButton = customtkinter.CTkRadioButton(master = radioButton_workspace,   #Create Radio button for pre recorded mode
                                                      variable=radioVar, 
                                                      value=1, 
                                                      text="Pre-Recorded Mode", 
                                                      text_font="Modern_Mono", 
                                                      command=self.videoMode)           #Call self.videoMode funtion when pressed

        videoRadButton.grid(row=1, column=3, pady=10, padx=20, sticky="n")              #Pack the radio button onto the page.

    def liveMode(self):

        if self.currentWorkspace != "live":         #If the current workspace is not the live mode, change it
            self.videoWorkspace.pack_forget()       #Destroy the videoWorkspace
            self.currentWorkspace = "live"          #Change current workspace to liveMode

            for widget in self.videoWorkspace.winfo_children():  #Destroy everything inside videoWorkspace
                widget.destroy()

            self.liveWorkspace.pack()               #Pack and load the liveMode workspace
            self.liveFeed = Label(self.liveWorkspace, width=1000, height=700, bg="#141B2D")    #Create box for putting camera feed in
            self.loadingFrame(status=True)          #Initiate the loading screen
            if self.videoModeVar == True:           #Allows the default video source to be set before being run
                self.cap = cv2.VideoCapture(0)      #Set video source to camera if not already
                self.videoModeVar = False           
            self.after(500, self.detect)            #Call the detect function

    def videoMode(self):

        def run():  #Funtion to open file selector
            filetypes = (('Video Files', '*.mp4'), ('All files', '*.*'))  #Set allowed filetypes
            filePath = filedialog.askopenfilename(filetypes=filetypes)    #Open file dialog and get path of video file
            for widgets in self.videoWorkspace.winfo_children():          #Destroy everything in the workspace
                widgets.destroy()

            self.liveFeed = Label(self.videoWorkspace, width=1000, height=700, bg="#141B2D")    #Set livefeed workspace
            self.loadingFrame(status=True)          #Call loading function
            self.cap = cv2.VideoCapture(filePath)   #Set video source to filepath specified
            self.videoModeVar = True                
            self.after(500, self.detect)            #Call detection function


        if self.currentWorkspace != "video":        #Change workspace mode
            self.liveWorkspace.pack_forget()
            self.currentWorkspace = "video"

            for widget in self.liveWorkspace.winfo_children():  #Destroy everything in liveWorkspace
                widget.destroy()

            self.videoWorkspace.pack()     #Pack the liveWorkspace
            modernFont = tkFont.Font(family="Modern_Mono", size=36) # Load font
            fileSelector = customtkinter.CTkButton(self.videoWorkspace,         #Create a button to initiate the file selector dialog
                                                   text="Select Video Source", 
                                                   height=400, 
                                                   width=800, 
                                                   text_font=modernFont, 
                                                   bg="#141B2D", 
                                                   command=run)                 #Call run function to open the fileselector
            fileSelector.pack(padx=500, pady=200)                               #Pack the button

    def switchDashboard(self, event):
        self.prevmast.switchFrame("homePage")

    def switchDetect(self, event):
        pass

    def switchDatabase(self, event):
        self.prevmast.switchFrame("databasePage")

    def switchSearch(self, event):
        self.prevmast.switchFrame("searchPage")

    def switchMOT(self, event):
        self.prevmast.switchFrame("motPage")
    
    def switchSettings(self, event):
        self.prevmast.switchFrame("settingsPage")

    def switchLogoff(self, event):
        self.prevmast.switchFrame("logoffPage")

if __name__ == "__main__":
    app = detectPage()
    app.mainloop()